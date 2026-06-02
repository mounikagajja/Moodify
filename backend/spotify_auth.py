import os
import httpx
from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

load_dotenv()

router = APIRouter()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

SCOPES = "user-read-private user-read-email user-top-read user-read-recently-played playlist-modify-public playlist-modify-private"

@router.get("/login")
def spotify_login():
    auth_url = (
        f"{SPOTIFY_AUTH_URL}"
        f"?client_id={SPOTIFY_CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={SPOTIFY_REDIRECT_URI}"
        f"&scope={SCOPES}"
    )
    return RedirectResponse(auth_url)

@router.get("/callback")
async def spotify_callback(code: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            SPOTIFY_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": SPOTIFY_REDIRECT_URI,
            },
            auth=(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET),
        )
    tokens = response.json()
    access_token = tokens.get("access_token")
    return RedirectResponse(f"http://localhost:5173/callback?token={access_token}")