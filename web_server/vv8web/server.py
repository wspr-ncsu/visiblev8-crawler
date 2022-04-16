from fastapi import FastAPI
from vv8web.routers import api_v1, webpage

app = FastAPI()

# enable CORS
from fastapi.middleware.cors import CORSMiddleware


app.include_router(webpage.router)
app.include_router(api_v1.router)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


