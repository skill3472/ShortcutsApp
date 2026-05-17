from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy.orm import Session

from admin import auth
from admin.models import LoginRequest
from database.repositories import admin_user as admin_user_repo
from database.session import get_session

admin_router = FastAPI()

_COOKIE = "session"


def get_current_user_id(request: Request) -> int:
    token = request.cookies.get(_COOKIE)
    if not token:
        raise HTTPException(401)
    try:
        return auth.decode_token(token)
    except jwt.PyJWTError:
        raise HTTPException(401)


@admin_router.post("/login")
def login(
    login_request: LoginRequest,
    response: Response,
    session: Annotated[Session, Depends(get_session)],
):
    user = admin_user_repo.get_by_username(session, login_request.username)
    if not user or not auth.verify_password(login_request.password, user.password_hash):
        raise HTTPException(403, "Invalid username or password")
    token = auth.create_token(user.id)
    response.set_cookie(_COOKIE, token, httponly=True, samesite="strict")
