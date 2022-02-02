from fastapi import FastAPI

from routers import api_v1, webpage

app = FastAPI()

print('webpage:', type(webpage.router), webpage.router)
print('api:', type(api_v1.router), api_v1.router)

app.include_router(webpage.router)
app.include_router(api_v1.router)
