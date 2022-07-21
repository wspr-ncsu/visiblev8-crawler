import imp
import re
import aiohttp
import asyncio
import urllib.parse

from celery import signature

from app.util.dns_lookup import dns_exists
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from typing import Optional
from app.core.celery_app import celery_app
# from vv8web_task_queue.tasks.vv8_worker_tasks import process_url_task
# from vv8web_task_queue.tasks.log_parser_tasks import parse_log_task


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
This outlines the characters allowed in the URL.
Reference: https://www.ietf.org/rfc/rfc3986.txt
"""
valid_url_chars = re.compile(
    r"^([:/?#\[\]@!$&\'()*+,;=A-Za-z0-9\-._~]|%[0-9a-fA-F][0-9a-fA-F])+$"
)


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
        and re.fullmatch(valid_url_chars, urlstr) != None
    )
    if not static_check:
        return False
    return await dns_exists(url.netloc)


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


"""
This method will request the URL, call the urlparse to parse the request, and check to make sure
that the URL's scheme is valid (and exists). If it does, then this method will proceed to call
is_url_valid and allow dns_exists to check to see if the URL is valid statically AND it is an 
actual URL that exists. If both are true, then we will check the cache to see if we have already
processed it in the past. If the URL is not valid, then we will flag it as not valid.
"""
@router.post('/urlcheck')
async def post_url_check(request: UrlRequestModel):
    url = request.url
    valid = await is_url_valid(url)
    if valid:
        async with aiohttp.ClientSession() as session:
            params = {'url': urllib.parse.quote(url)}
            async with session.get('http://database_sidecar:80/api/v1/submission', params=params) as resp:
                resp.raise_for_status()
                resp_data = await resp.json()
                submission_id = resp_data['submission_id']
                if submission_id is None:
                    cached = False
                else:
                    cached = True
        return UrlResponseModel(
            valid=True,
            cached=cached
        )
    return UrlResponseModel(
        valid=False,
        cached=False
    )


"""
Here we define the Results of our validation, and get both the URL
and whether or not we need to rerun it ready to return to the frontend.
"""
class UrlSubmitRequestModel(BaseModel):
    url: str
    rerun: Optional[bool] = False


@dataclass
class UrlSubmitResponseModel:
    submission_id: int


# Handles processing url submission and returns submission id
@router.post('/urlsubmit', response_model=UrlSubmitResponseModel)
async def post_url_submit(request: UrlSubmitRequestModel):
    url = request.url
    rerun = request.rerun
    if not await is_url_valid(url):
        raise HTTPException(status_code=400, detail='Invalid URL')
    submission_id = None
    async with aiohttp.ClientSession() as session:
        if not rerun:
            # If not rerun we need to check for a cached version of this url
            params = {'url': urllib.parse.quote(url)}
            async with session.get('http://database_sidecar:80/api/v1/submission', params=params) as resp:
                resp.raise_for_status()
                resp_data = await resp.json()
                submission_id = resp_data['submission_id']
                assert submission_id is None or isinstance(submission_id, int)
        if rerun or submission_id is None:
            # Create submission id
            async with session.post('http://database_sidecar:80/api/v1/submission', json={'url': url}) as resp:
                resp.raise_for_status()
                sub_resp = await resp.json()
                submission_id = sub_resp['submission_id']
            # Run the pipeline
            # TODO totally unsure if this will work, this sends a task to the task queue via name instead
            # of needing to have all the code duplicated into the web server project
            url_pipeline = celery_app.send_task('tasks.process_url_task', chain=[
                signature('parse_log_task', kwargs={'tasks.submission_id': submission_id})
            ])
            # url_pipeline = chain(process_url_task.s(), parse_log_task.s(submission_id))


            async_res = url_pipeline.apply_async((url, submission_id))
            # pipeline completion poll interval
            poll_interval = 0.5
            while not async_res.ready():
                await asyncio.sleep(poll_interval)
            # We do not need the result, so just forget it.
            # Need to call get() or forget() to release resources maintaining async state
            async_res.forget()
        # return submission id
        assert isinstance(submission_id, int)
        return UrlSubmitResponseModel(submission_id)


