from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from typing import Optional


router = APIRouter()
templates = Jinja2Templates(directory="vv8web/templates")


@router.get('/results')
def get_results(url: str, rerun: Optional[bool] = False):
    pass


