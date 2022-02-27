import urllib.parse as urlparse
import re
from vv8web.util.dns_lookup import dns_exists
from fastapi import APIRouter
from fastapi import APIRouter, Form
from pydantic import BaseModel
from typing import Optional


router = APIRouter(
    prefix='/api/v1'
)

valid_schemas = {
    'http',
    'https'
}

# Reference: https://www.ietf.org/rfc/rfc3986.txt
valid_url_chars = re.compile(
    r"^([:/?#\[\]@!$&\'()*+,;=A-Za-z0-9\-._~]|%[0-9a-fA-F][0-9a-fA-F])+$"
)


def is_url_valid(urlstr):
    url = urlparse.urlparse(urlstr)
    return (
        len(urlstr) != 0
        and url.scheme in valid_schemas
        and len(url.netloc) != 0
        and re.fullmatch(valid_url_chars, urlstr) != None
    )


class UrlModel(BaseModel):
    url: str


class UrlResponseModel(BaseModel):
    valid: bool
    cached: Optional[bool]


@router.post('/url')
async def post_url(request: str = Form(...)):
    # Static URL analysis
    parsed_url = urlparse.urlparse(request)
    if len(parsed_url.scheme) == 0:
        # TODO: prepend http or https on url if needed
        pass
    valid = is_url_valid(request) and await dns_exists(parsed_url.netloc)
    if valid:
        # TODO: Check cache
        return UrlResponseModel(
            valid=True,
            cached=False
        )
    return UrlResponseModel(
        valid=False
    )


class ResultsModel(BaseModel):
    url: str
    rerun: Optional[bool] = False


@router.post('/results')
def post_results(request: ResultsModel):
    pass
