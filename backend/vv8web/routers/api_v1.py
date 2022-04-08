import re
import requests
import celery
import asyncio

from vv8web.util.dns_lookup import dns_exists
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from urllib.parse import urlparse
from vv8web_task_queue.tasks.vv8_worker_tasks import process_url_task
from vv8web_task_queue.tasks.log_parser_tasks import parse_log_task


"""
This file will contain the basic data and functionality to validate URLs.
"""

# This defines the router object and sets its prefix.
router = APIRouter(
    prefix='/api/v1'
)


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
    url = urlparse(urlstr)
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
@router.post('/url')
async def post_url(request: UrlRequestModel):
    valid = await is_url_valid(request.url)
    if valid:
        # TODO: Check cache
        return UrlResponseModel(
            valid=True,
            cached=False
        )
    return UrlResponseModel(
        valid=False
    )


"""
Here we define the Results of our validation, and get both the URL
and whether or not we need to rerun it ready to return to the frontend.
"""
class ResultsRequestModel(BaseModel):
    url: str
    rerun: Optional[bool] = False


# Here we send the ResultsModel defined above back to the frontend.
@router.post('/results')
async def post_results(request: ResultsRequestModel):
    url = request.url
    if not await is_url_valid(url):
        raise HTTPException(status_code=400, detail='Invalid URL')
    if request.rerun:
        # Create submission
        sub_resp = requests.post(
            'http://database_sidecar:80/api/v1/submission',
            json={'url': url}
        )
        sub_resp.raise_for_status()
        sub_resp_data = sub_resp.json()
        submission_id = sub_resp_data['submission_id']
        #schedule_process_url_task(submission.url, submission_id)
        url_pipeline = celery.chain(process_url_task.s(), parse_log_task.s(submission_id))
        async_res = url_pipeline.apply_async((url, submission_id))
        while not async_res.ready():
            # poll every 0.25 seconds if url pipeline is complete
            await asyncio.sleep(0.25)
        # We do not need the result, so just forget it.
        # Need to call get() or forget() to release resources maintaining async state
        async_res.forget()
        # TODO: Get result data
    else:
        # Query database for results
        pass
