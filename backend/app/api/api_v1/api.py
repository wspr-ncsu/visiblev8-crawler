from fastapi import APIRouter

from app.api.api_v1.endpoints import tasks
from app.api.api_v1.endpoints import results

api_router = APIRouter()
api_router.include_router(tasks.router)
api_router.include_router(results.router, prefix="/results")
