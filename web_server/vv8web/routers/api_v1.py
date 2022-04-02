import urllib.parse as urlparse
import re

from vv8web.util.dns_lookup import dns_exists
from fastapi import APIRouter
from fastapi import APIRouter, Form
from pydantic import BaseModel
from typing import Optional
from urllib.parse import urlparse
from vv8web_task_queue.tasks.vv8_worker_tasks import schedule_process_url_task


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
    url = urlparse.urlparse(urlstr)
    static_check = (
        len(urlstr) != 0
        and url.scheme in valid_schemas
        and len(url.netloc) != 0
        and re.fullmatch(valid_url_chars, urlstr) != None
    )
    if not static_check:
        return False
    parsed_url = urlparse.urlparse(request)
    return await dns_exists(parsed_url.netloc)

"""
Here we will define the URL as a string so we can scan it later on.
"""
class UrlModel(BaseModel):
    url: str

"""
Here we define the model we will use to return an initial check of the URL,
and return whether or not the URL passed validation checks and, if so, if we found
the URL in the cache.
"""
class UrlResponseModel(BaseModel):
    valid: bool
    cached: Optional[bool]


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
async def post_url(request: str = Form(...)):
    valid = await is_url_valid(request)
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
class ResultsModel(BaseModel):
    url: str
    rerun: Optional[bool] = False

# Here we send the ResultsModel defined above back to the frontend.
@router.post('/results')
async def post_results(submission: ResultsModel):
    if request.rerun:
        # Run vv8 on url
        scheme, domain, path, _, query, fragment = urlparse(url)
        # TODO: create submission entry in database
        # TODO: get submission id
        submission_id = -1
        schedule_process_url_task(submission.url, submission_id)
        # TODO: async-wait for url to be processed
        # This will likely involve asyncio.Event
        # ref: https://docs.python.org/3/library/asyncio-sync.html#asyncio.Event
    else:
        # Query database for results
        pass

