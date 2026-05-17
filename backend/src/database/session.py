from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from config import settings


engine = create_engine(settings.database_url)
_SessionLocal = sessionmaker(bind=engine)


def get_session() -> Generator[Session, None, None]:
    with _SessionLocal() as session:
        yield session
