from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional


router = APIRouter(
    prefix='/api/v1'
)


class UrlModel(BaseModel):
    url: str


class UrlResponseModel(BaseModel):
    valid: bool
    cached: Optional[bool]


@router.post('/url')
def post_url(request: UrlModel):
    return UrlResponseModel(
        valid=False
    )


class ResultsModel(BaseModel):
    url: str
    rerun: Optional[bool] = False


@router.post('results')
def post_results(request: ResultsModel):
    pass
