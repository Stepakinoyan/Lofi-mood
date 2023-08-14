import time
from fastapi import APIRouter, Depends, Request
from spotipy.oauth2 import SpotifyOAuth
from fastapi.responses import RedirectResponse
from app.parser.lofi import Recommendations
from config import CLIENT_ID, CLIENT_SECRET

lofi = APIRouter(prefix='/spotify', tags=['Lofi funcs'])


redirect_uri='http://localhost:8000/spotify/authorize'

@lofi.get('/login')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return RedirectResponse(auth_url)

def get_session(request: Request):
    return request.session


@lofi.get('/authorize')
def auth(request: Request):
    sp_oauth = create_spotify_oauth()
    session = request.session
    session.clear()
    code = request.query_params.get('code')
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return RedirectResponse("/spotify/getTracks")

@lofi.get('/getTracks')
def get_tracks(request: Request):
    session = request.session
    token_info, authorized = get_token(session)
    if not authorized:
        return RedirectResponse('/')
    
    sp = Recommendations(auth=token_info.get('access_token'), mood='sad')
    return sp.get_lofi()


def get_token(session = Depends(get_session)):
    token_info = session.get("token_info", {})
    token_valid = False

    # Checking if the session already has a token stored
    if not token_info:
        return token_info, token_valid

    # Checking if token has expired
    now = int(time.time())
    is_token_expired = token_info.get('expires_at', 0) - now < 60

    # Refreshing token if it has expired
    if is_token_expired:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info.get('refresh_token'))

    token_valid = True
    return token_info, token_valid


def create_spotify_oauth():
    return SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, redirect_uri, scope='playlist-modify-public')