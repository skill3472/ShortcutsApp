from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from admin import auth
from admin.models import LoginRequest
from database.repositories import admin_user as admin_user_repo
from database.session import get_session

admin_router = APIRouter(prefix="/admin")


@admin_router.post("/login")
def login(
    login_request: LoginRequest,
    response: Response,
    session: Annotated[Session, Depends(get_session)],
):
    user = admin_user_repo.get_by_username(session, login_request.username)
    if not user or not auth.verify_password(login_request.password, user.password_hash):
        raise HTTPException(403, "Invalid username or password")
    token = auth.create_token(user.user_id)
    response.set_cookie("session", token, httponly=True, samesite="strict")
