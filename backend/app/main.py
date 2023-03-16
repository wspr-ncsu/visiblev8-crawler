from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.api_v1.api import api_router
from app.core.config import settings

# enable CORS
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
app.mount("/parsed_logs/", StaticFiles(directory="/parsed_logs"), name="parsed_logs")
app.mount("/raw_logs/", StaticFiles(directory="/raw_logs"), name="raw_logs")
app.mount("/screenshots/", StaticFiles(directory="/screenshots"), name="screenshots")
app.mount("/har/", StaticFiles(directory="/har"), name="har")