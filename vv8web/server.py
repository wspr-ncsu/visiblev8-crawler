from fastapi import FastAPI

from vv8web.routers import api_v1, webpage

app = FastAPI()

app.include_router(webpage.router)
app.include_router(api_v1.router)
