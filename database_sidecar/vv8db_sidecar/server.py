from fastapi import FastAPI
from vv8db_sidecar.routers import api_v1

app = FastAPI()

app.include_router(api_v1.router)
