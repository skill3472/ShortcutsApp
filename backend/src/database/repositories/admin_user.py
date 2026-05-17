from sqlalchemy.orm import Session

from database.schema import AdminUser


def create(session: Session, username: str, password_hash: str) -> AdminUser:
    user = AdminUser(username=username, password_hash=password_hash)
    session.add(user)
    session.flush()
    session.refresh(user)
    return user


def get_by_username(session: Session, username: str) -> AdminUser | None:
    return session.query(AdminUser).filter_by(username=username).first()
