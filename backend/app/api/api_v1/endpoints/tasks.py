from datetime import datetime
import urllib.parse

from celery import signature
from uuid import uuid4 as uuid

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from typing import Optional
from app.core.celery_app import celery_client
from app.core.database import sql_session, mongo_db

from app.database_models.database_models import Submission

"""
This file will contain the basic data and functionality to validate URLs.
"""

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


"""
Here we define the model we will use to return an initial check of the URL,
and return whether or not the URL passed validation checks and, if so, if we found
the URL in the cache.
"""
class UrlResponseModel(BaseModel):
    valid: bool
    cached: Optional[bool]


"""
Here we will define the URL as a string so we can scan it later on.
"""
class UrlRequestModel(BaseModel):
    url: str

class ParserConfig(BaseModel):
    parser: str
    delete_log_after_parsing: bool
    output_format_to_mongoresql: bool

"""
Here we define the Results of our validation, and get both the URL
and whether or not we need to rerun it ready to return to the frontend.
"""
class UrlSubmitRequestModel(BaseModel):
    url: str
    rerun: Optional[bool] = False
    parser_config: Optional[ParserConfig]


@dataclass
class UrlSubmitResponseModel:
    cached: bool
    submission_id: str


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
        if rerun or submission_id is None:
            # Create submission id
            submission = Submission(id=str(uuid()), url=url, start_time=datetime.now())
            session.add(submission)
            session.commit()
            submission_id = submission.id
        if request.parser_config is not None:
            celery_client.send_task(
                name='vv8_worker.process_url',
                kwargs={'url': url, 'submission_id': submission_id},
                queue="crawler",
                chain=[
                    signature('log_parser_worker.parse_log', kwargs={'submission_id': submission_id, 'config': request.parser_config.dict()}, queue="log_parser")
                ])
        else:
            celery_client.send_task(
                name='vv8_worker.process_url',
                kwargs={'url': url, 'submission_id': submission_id},
                queue="crawler")
    return UrlSubmitResponseModel(cached, submission_id)