from sqlalchemy.orm import Session, selectinload

from database.schema import Application, Shortcut, ShortcutCategory


def _shortcut_options():
    return selectinload(Shortcut.category).selectinload(ShortcutCategory.app)


# Applications


def create_application(session: Session, name: str, color: str) -> Application:
    app = Application(name=name, color=color)
    session.add(app)
    session.flush()
    session.refresh(app)
    return app


def get_applications(session: Session) -> list[Application]:
    return session.query(Application).all()


def get_application(session: Session, app_id: int) -> Application | None:
    return session.get(Application, app_id)


def delete_application(session: Session, app_id: int) -> bool:
    app = session.get(Application, app_id)
    if not app:
        return False
    session.delete(app)
    return True


# Categories


def create_category(session: Session, name: str, app_id: int) -> ShortcutCategory:
    category = ShortcutCategory(name=name, app_id=app_id)
    session.add(category)
    session.flush()
    session.refresh(category)
    return category


def get_categories(session: Session, app_id: int) -> list[ShortcutCategory]:
    return session.query(ShortcutCategory).filter_by(app_id=app_id).all()


def get_category(session: Session, category_id: int) -> ShortcutCategory | None:
    return session.get(ShortcutCategory, category_id)


def delete_category(session: Session, category_id: int) -> bool:
    category = session.get(ShortcutCategory, category_id)
    if not category:
        return False
    session.delete(category)
    return True


# Shortcuts


def create_shortcut(
    session: Session, name: str, keystrokes: list[str], category_id: int
) -> Shortcut:
    shortcut = Shortcut(name=name, keystrokes=keystrokes, category_id=category_id)
    session.add(shortcut)
    session.flush()
    return (
        session.query(Shortcut)
        .options(_shortcut_options())
        .filter_by(shortcut_id=shortcut.shortcut_id)
        .one()
    )


def get_shortcuts(session: Session, category_id: int) -> list[Shortcut]:
    return (
        session.query(Shortcut)
        .options(_shortcut_options())
        .filter_by(category_id=category_id)
        .all()
    )


def get_shortcut(session: Session, shortcut_id: int) -> Shortcut | None:
    return (
        session.query(Shortcut)
        .options(_shortcut_options())
        .filter_by(shortcut_id=shortcut_id)
        .one_or_none()
    )


def update_shortcut(
    session: Session,
    shortcut_id: int,
    name: str | None,
    keystrokes: list[str] | None,
) -> Shortcut | None:
    shortcut = session.get(Shortcut, shortcut_id)
    if not shortcut:
        return None
    if name is not None:
        shortcut.name = name
    if keystrokes is not None:
        shortcut.keystrokes = keystrokes
    session.flush()
    return (
        session.query(Shortcut)
        .options(_shortcut_options())
        .filter_by(shortcut_id=shortcut_id)
        .one()
    )


def delete_shortcut(session: Session, shortcut_id: int) -> bool:
    shortcut = session.get(Shortcut, shortcut_id)
    if not shortcut:
        return False
    session.delete(shortcut)
    return True
