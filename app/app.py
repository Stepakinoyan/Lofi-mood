from fastapi import FastAPI, Request, HTTPException, Cookie
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from spotipy import SpotifyOAuth
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
import spotipy
from fastapi.staticfiles import StaticFiles
from parser.lofi import get_playlist_by_mood
import datetime
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:8000'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sp_oauth = SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope='playlist-modify-private')
template = Jinja2Templates(directory='app/templates')


@app.get('/')
async def index_page(request: Request):
        return template.TemplateResponse('index.html', {'request': request})


@app.get("/login")
async def spotify_login():
    auth_url = sp_oauth.get_authorize_url()
    return RedirectResponse(auth_url)


@app.get("/authorize")
async def authorize(request: Request):
            params = dict(request.query_params)
            token_code = params.get('code')
            if token_code:
                    token_info = sp_oauth.get_access_token(token_code)
                    
                    sp = spotipy.Spotify(auth=token_info['access_token'])
                    template_response = template.TemplateResponse('authorize.html', {'request': request, 'username': sp.me()['display_name']})
                    expiration_date = datetime.datetime.utcnow() + datetime.timedelta(days=3650)
                    expiration_str = expiration_date.strftime("%a, %d %b %Y %H:%M:%S GMT")

                    template_response.set_cookie(key="token", value=token_info['access_token'], httponly=True, expires=expiration_str)

                    return template_response
    
            return HTTPException(status_code=500, detail='Authorize error')


@app.get('/getPlaylist/{mood}/{playlist_name}')
async def send_playlist_to_spotify(mood: str, playlist_name: str, token: Optional[str] = Cookie(None)):
        result = await get_playlist_by_mood(mood=mood, playlist_name=playlist_name, token=token)
        return result


@app.get('/getToken')
async def get_token_from_cookies(token: Optional[str] = Cookie(None)):
        return token