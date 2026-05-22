from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session

from admin import get_current_user_id
from database.repositories import shortcuts as repo
from database.session import get_session
from shortcuts.models import (
    Application,
    CreateApplication,
    CreateShortcut,
    CreateShortcutCategory,
    Shortcut,
    ShortcutCategory,
    UpdateShortcut,
)

shortcuts_router = APIRouter(prefix="/shortcuts")

SessionDep = Annotated[Session, Depends(get_session)]
AuthDep = Annotated[int, Security(get_current_user_id)]


# Applications

@shortcuts_router.post("/applications", response_model=Application)
def create_application(body: CreateApplication, session: SessionDep, _: AuthDep):
    app = repo.create_application(session, body.name, body.color)
    session.commit()
    return app


@shortcuts_router.get("/applications", response_model=list[Application])
def list_applications(session: SessionDep):
    return repo.get_applications(session)


@shortcuts_router.get("/applications/{app_id}", response_model=Application)
def get_application(app_id: int, session: SessionDep):
    app = repo.get_application(session, app_id)
    if not app:
        raise HTTPException(404)
    return app


@shortcuts_router.delete("/applications/{app_id}", status_code=204)
def delete_application(app_id: int, session: SessionDep, _: AuthDep):
    if not repo.delete_application(session, app_id):
        raise HTTPException(404)
    session.commit()


# Categories

@shortcuts_router.post("/categories", response_model=ShortcutCategory)
def create_category(body: CreateShortcutCategory, session: SessionDep, _: AuthDep):
    if not repo.get_application(session, body.app_id):
        raise HTTPException(404, "Application not found")
    category = repo.create_category(session, body.name, body.app_id)
    session.commit()
    return category


@shortcuts_router.get("/applications/{app_id}/categories", response_model=list[ShortcutCategory])
def list_categories(app_id: int, session: SessionDep):
    return repo.get_categories(session, app_id)


@shortcuts_router.get("/categories/{category_id}", response_model=ShortcutCategory)
def get_category(category_id: int, session: SessionDep):
    category = repo.get_category(session, category_id)
    if not category:
        raise HTTPException(404)
    return category


@shortcuts_router.delete("/categories/{category_id}", status_code=204)
def delete_category(category_id: int, session: SessionDep, _: AuthDep):
    if not repo.delete_category(session, category_id):
        raise HTTPException(404)
    session.commit()


# Shortcuts

@shortcuts_router.post("/shortcuts", response_model=Shortcut)
def create_shortcut(body: CreateShortcut, session: SessionDep, _: AuthDep):
    if not repo.get_category(session, body.category_id):
        raise HTTPException(404, "Category not found")
    shortcut = repo.create_shortcut(session, body.name, body.keystrokes, body.category_id)
    session.commit()
    return shortcut


@shortcuts_router.get("/categories/{category_id}/shortcuts", response_model=list[Shortcut])
def list_shortcuts(category_id: int, session: SessionDep):
    return repo.get_shortcuts(session, category_id)


@shortcuts_router.get("/shortcuts/{shortcut_id}", response_model=Shortcut)
def get_shortcut(shortcut_id: int, session: SessionDep):
    shortcut = repo.get_shortcut(session, shortcut_id)
    if not shortcut:
        raise HTTPException(404)
    return shortcut


@shortcuts_router.patch("/shortcuts/{shortcut_id}", response_model=Shortcut)
def update_shortcut(shortcut_id: int, body: UpdateShortcut, session: SessionDep, _: AuthDep):
    shortcut = repo.update_shortcut(session, shortcut_id, body.name, body.keystrokes)
    if not shortcut:
        raise HTTPException(404)
    session.commit()
    return shortcut


@shortcuts_router.delete("/shortcuts/{shortcut_id}", status_code=204)
def delete_shortcut(shortcut_id: int, session: SessionDep, _: AuthDep):
    if not repo.delete_shortcut(session, shortcut_id):
        raise HTTPException(404)
    session.commit()
