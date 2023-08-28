from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .auth.db import User, create_db_and_tables
from .auth.schemas import UserCreate, UserRead, UserUpdate
from .auth.userManager import (
    auth_backend,
    current_active_user,
    fastapi_users,
    spotify_oauth_client,
)
import sys
sys.path.append('/mnt/c/Stepa/lofi_mood/code')
from config import SECRET_CODE


app = FastAPI()

template = Jinja2Templates(directory='app/templates')


app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
app.include_router(
    fastapi_users.get_oauth_router(oauth_client=spotify_oauth_client, backend=auth_backend, state_secret=SECRET_CODE),
    prefix="/auth/spotify",
    tags=["auth"],
)

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return template.TemplateResponse('index.html', {'request': request})



@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.id}!"} 


@app.on_event("startup")
async def on_startup():
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()