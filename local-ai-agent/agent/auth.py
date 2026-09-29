import os
import secrets
import uuid
from pathlib import Path
from dotenv import load_dotenv
from fastapi import HTTPException, Request, Response
from starlette.status import HTTP_401_UNAUTHORIZED

DOTENV_PATH = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(DOTENV_PATH, override=True)

SESSION_COOKIE_NAME = os.getenv("SESSION_COOKIE_NAME", "local_ai_agent_session")

sessions: dict[str, str] = {}

def _validate_credentials(username: str, password: str) -> bool:
    load_dotenv(DOTENV_PATH, override=True)
    control_username = os.getenv("CONTROL_USERNAME", "admin").strip()
    control_password = os.getenv("CONTROL_PASSWORD", "password").strip()
    return (
        secrets.compare_digest(username.strip(), control_username)
        and secrets.compare_digest(password.strip(), control_password)
    )

def create_session(username: str) -> str:
    token = secrets.token_urlsafe(32)
    sessions[token] = username
    return token

def get_current_user(request: Request) -> str:
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if not token or token not in sessions:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return sessions[token]

async def authenticate_request(request: Request) -> str:
    return get_current_user(request)

async def login_user(username: str, password: str, response: Response) -> dict:
    if not _validate_credentials(username, password):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    token = create_session(username)
    response.set_cookie(
        SESSION_COOKIE_NAME,
        token,
        httponly=True,
        samesite="lax",
        path='/',
    )
    return {"status": "ok", "username": username}

async def logout_user(request: Request, response: Response) -> dict:
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if token and token in sessions:
        sessions.pop(token, None)
    response.delete_cookie(SESSION_COOKIE_NAME)
    return {"status": "logged_out"}
