from datetime import datetime
from multiprocessing.pool import AsyncResult
import urllib.parse

from celery import signature
from uuid import uuid4 as uuid
import glob
import os
import urllib.parse
from datetime import datetime
from multiprocessing.pool import AsyncResult
from typing import List, Optional
from uuid import uuid4 as uuid

from app.core.celery_app import celery_client
from app.core.database import mongo_db, sql_session
from app.database_models.backend_database_models import Submission
from celery import signature
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pydantic.dataclasses import dataclass

# This defines the router object and sets its prefix.
router = APIRouter()


# The set outlines the valid schemas a URL can have.
# Without them, we will classify the URL as invalid.
valid_schemas = {
    'http',
    'https'
}

"""
This method will test the input URL to make sure that:
1. It is not a length of zero.
2. The Scheme of the URL (the prefix) is either https or http.
3. The URL's netlock is not a length of zero.
4. All of the characters in the URL are valid characters.
"""


async def is_url_valid(urlstr):
    url = urllib.parse.urlparse(urlstr)
    static_check = (
        len(urlstr) != 0
        and url.scheme in valid_schemas
        and len(url.netloc) != 0
    )
    if not static_check:
        return False
    return True


class UrlResponseModel(BaseModel):
    '''
    Here we define the model we will use to return an initial check of the URL,
    and return whether or not the URL passed validation checks and, if so, if we found
    the URL in the cache.
    '''
    valid: bool
    cached: Optional[bool]


class UrlRequestModel(BaseModel):
    '''
    Here we will define the URL as a string so we can scan it later on.
    '''
    url: str

class ParserConfigRequest(BaseModel):
    parser: str
    delete_log_after_parsing: Optional[bool]
    output_format: Optional[str]

class ParserConfigCelery(BaseModel):
    parser: Optional[str]
    delete_log_after_parsing: Optional[bool]
    output_format: Optional[str]
    mongo_id: Optional[str]

def copy_from_request_to_celery(request: ParserConfigRequest) -> ParserConfigCelery:
    ret = ParserConfigCelery()
    request.delete_log_after_parsing = request.delete_log_after_parsing or False
    request.output_format = request.output_format or 'postgresql'
    ret.__dict__.update(request.__dict__)
    return ret


class UrlSubmitRequestModel(BaseModel):
    '''
        Here we define the Results of our validation, and get both the URL
        and whether or not we need to rerun it ready to return to the frontend.
    '''
    url: str
    rerun: Optional[bool] = False
    crawler_args: Optional[List[str]] = []
    disable_har: Optional[bool] = False
    disable_screenshot: Optional[bool] = False
    disable_artifact_collection: Optional[bool] = False
    parser_config: Optional[ParserConfigRequest]
    hard_timeout: Optional[int] = 2 * 60 # timeout


@dataclass
class UrlSubmitResponseModel:
    cached: bool
    submission_id: str

@dataclass
class UrlStatusResponseModel:
    vv8_worker_status: str
    vv8_worker_info: Optional[dict]
    log_parser_was_executed: bool
    log_parser_worker_status: Optional[str]
    log_parser_worker_info: Optional[dict]
    postprocessors_used: Optional[str]
    postprocessors_output_format: Optional[str]
    postprocessors_delete_log_after_parsing: Optional[bool]
    crawler_args: Optional[List[str]]
    mongo_id: Optional[str]
    screenshot_url: Optional[str]
    har_url: Optional[str]
    raw_log_urls: Optional[List[str]]
    parsed_log_url: Optional[str]


@dataclass
class UrlStatusRequestModel:
    url: str


# Handles processing url submission and returns submission id
@router.post('/urlsubmit', response_model=UrlSubmitResponseModel)
async def post_url_submit(request: UrlSubmitRequestModel):
    url = request.url
    rerun = request.rerun
    if not await is_url_valid(url):
        raise HTTPException(status_code=400, detail='Invalid URL')
    submission_id = None
    cached = False
    with sql_session() as session:
        submission = None
        if not rerun:
            # If not rerun we need to check for a cached version of this url
            submission = session.query(Submission.id).filter(Submission.url == url).first()
            if submission is not None:
                submission_id = submission[0].id
                cached = True
                return UrlSubmitResponseModel(cached, submission_id)
        if rerun or submission_id is None:
            submission_id = str(uuid())
            celery_req: AsyncResult = None
            mongo_id = None
            # do mongo stuff
            mongo_id = mongo_db['vv8_logs'].insert_one({'url': request.url}).inserted_id
            if request.parser_config is not None:
                parserconfigcelery = copy_from_request_to_celery(request.parser_config)
                parserconfigcelery.mongo_id = str(mongo_id)
                log_parser_uid = str(uuid())
                celery_req = celery_client.send_task(
                    name='vv8_worker.process_url',
                    kwargs={
                        'url': url,
                        'submission_id': submission_id,
                        'config': {
                            'mongo_id': str(mongo_id),
                            'disable_har': request.disable_har,
                            'disable_screenshot': request.disable_screenshot,
                            'disable_artifact_collection': request.disable_artifact_collection,
                            'crawler_args': request.crawler_args,
                            'delete_log_after_parsing': request.parser_config.delete_log_after_parsing,
                            'hard_timeout': request.hard_timeout
                        }
                    },
                    queue="crawler",
                    chain=[
                        signature('log_parser_worker.parse_log',
                            kwargs={
                                'submission_id': submission_id,
                                'config': parserconfigcelery.dict()
                                },
                            queue="log_parser"
                        ).set(task_id=log_parser_uid)
                    ])
                submission = Submission(
                    id=submission_id,
                    url=url,
                    start_time=datetime.now(),
                    vv8_req_id=celery_req.id,
                    log_parser_req_id=log_parser_uid,
                    mongo_id=str(mongo_id),
                    postprocessor_used=request.parser_config.parser,
                    postprocessor_output_format=request.parser_config.output_format,
                    postprocessor_delete_log_after_parsing=request.parser_config.delete_log_after_parsing,
                    crawler_args=request.crawler_args)
            else:
                celery_req = celery_client.send_task(
                    name='vv8_worker.process_url',
                    kwargs={
                        'url': url,
                        'submission_id': submission_id,
                        'config': {
                            'mongo_id': str(mongo_id),
                            'disable_har': request.disable_har,
                            'disable_screenshot': request.disable_screenshot,
                            'disable_artifact_collection': request.disable_artifact_collection,
                            'crawler_args': request.crawler_args,
                            'delete_log_after_parsing': False,
                            'hard_timeout': request.hard_timeout
                        }
                    },
                    queue="crawler")
                submission = Submission(
                    id=submission_id,
                    url=url, start_time=datetime.now(),
                    vv8_req_id=celery_req.id,
                    mongo_id=str(mongo_id),
                    crawler_args=request.crawler_args)
            session.add(submission)
            session.commit()
            return UrlSubmitResponseModel(cached, submission_id)

@router.post('/status/{submission_id}', response_model=UrlStatusResponseModel)
async def get_submission_status(submission_id: str):
    with sql_session() as session:
        submission = session.query(Submission).filter(Submission.id == submission_id).first()
        if submission is None:
            raise HTTPException(status_code=404, detail='Submission not found')
        vv8_celery_req = celery_client.AsyncResult(submission.vv8_req_id)
        log_parser_was_executed = True if submission.log_parser_req_id else False
        log_celery_req = celery_client.AsyncResult(submission.log_parser_req_id or '00000000-0000-0000-0000-000000000000') # invalid uuid
        vv8_celery_req_info = None
        log_celery_req_info = None
        if isinstance( vv8_celery_req.info, Exception):
            vv8_celery_req_info = { 'status': str(vv8_celery_req.info) }
        else:
            vv8_celery_req_info = vv8_celery_req.info
        if isinstance( log_celery_req.info, Exception ):
            log_celery_req_info = { 'status': str(vv8_celery_req.info) }
        else:
            log_celery_req_info = log_celery_req.info
        if vv8_celery_req.status == 'SUCCESS':
            raw_logs_dir = os.path.join('/raw_logs', submission.id)
            filelist = glob.glob(os.path.join(raw_logs_dir, 'vv8*.log'))
            raw_log_urls = []
            parsed_log_path = os.path.join('/parsed_logs', submission.id, 'parsed_log.output')
            for f in filelist:
                raw_log_urls.append(os.path.join('/raw_logs', submission.id, f.split("/")[-1]))
            return UrlStatusResponseModel(
                vv8_worker_status=vv8_celery_req.status,
                vv8_worker_info=vv8_celery_req_info,
                log_parser_was_executed=log_parser_was_executed,
                log_parser_worker_status=log_celery_req.status,
                log_parser_worker_info=log_celery_req_info,
                mongo_id=submission.mongo_id,
                postprocessors_used=submission.postprocessor_used,
                postprocessors_output_format=submission.postprocessor_output_format,
                postprocessors_delete_log_after_parsing=submission.postprocessor_delete_log_after_parsing,
                crawler_args=submission.crawler_args,
                screenshot_url=os.path.join('/screenshots', f'{submission.id}.png'),
                har_url=os.path.join('/har', f'{submission.id}.har'),
                raw_log_urls=raw_log_urls,
                parsed_log_url=parsed_log_path if os.path.exists(parsed_log_path) else ''
            )
        return UrlStatusResponseModel(
            vv8_worker_status=vv8_celery_req.status,
            vv8_worker_info=vv8_celery_req_info,
            log_parser_worker_status=log_celery_req.status,
            log_parser_was_executed=log_parser_was_executed,
            log_parser_worker_info=log_celery_req_info,
            mongo_id=submission.mongo_id,
            postprocessors_used='',
            postprocessors_output_format='',
            postprocessors_delete_log_after_parsing=False,
            crawler_args=[],
            screenshot_url='',
            har_url='',
            raw_log_urls=[],
            parsed_log_url='')
