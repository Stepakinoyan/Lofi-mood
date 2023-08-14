from fastapi import FastAPI
from .router import lofi
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="eQ$2R#9pA6mZu8xYs")

# @app.get("/")
# async def read_root():
#     return {"message": "Welcome to the Spotify API with FastAPI!"}

app.include_router(lofi)