from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from typing import Optional


router = APIRouter()


@router.get('/')
def get_root():
    return HTMLResponse('hello world')


@router.get('/results')
def get_results(url: str, rerun: Optional[bool] = False):
    pass
