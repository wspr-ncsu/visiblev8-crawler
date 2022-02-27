from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from vv8web.routers import api_v1, webpage

app = FastAPI()

app.include_router(webpage.router)
app.include_router(api_v1.router)

app.mount("/", StaticFiles(directory="vv8web/static", html=True), name="static")
app.mount("/static", StaticFiles(directory="vv8web/static/resources", html=True), name="resources")
