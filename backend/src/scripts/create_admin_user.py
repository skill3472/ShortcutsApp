import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from admin.auth import hash_password
from database.repositories import admin_user as admin_user_repo
from database.schema import Base
from database.session import _SessionLocal, engine


def main():
    username = input("Username: ")
    password = input("Password: ")

    Base.metadata.create_all(engine)

    with _SessionLocal() as session:
        user = admin_user_repo.create(session, username, hash_password(password))
        session.commit()
        print(f"Created admin user '{user.username}' (id={user.user_id})")


if __name__ == "__main__":
    main()
