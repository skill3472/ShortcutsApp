from datetime import datetime

from sqlalchemy import ForeignKey, JSON, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class AdminUser(Base):
    __tablename__ = "admins"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    password_hash: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class Application(Base):
    __tablename__ = "applications"

    application_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    color: Mapped[str]
    categories: Mapped[list["ShortcutCategory"]] = relationship(
        back_populates="app", cascade="all, delete-orphan"
    )


class ShortcutCategory(Base):
    __tablename__ = "shortcut_categories"

    category_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    app_id: Mapped[int] = mapped_column(
        ForeignKey("applications.application_id", ondelete="CASCADE")
    )
    app: Mapped["Application"] = relationship(back_populates="categories")
    shortcuts: Mapped[list["Shortcut"]] = relationship(
        back_populates="category", cascade="all, delete-orphan"
    )


class Shortcut(Base):
    __tablename__ = "shortcuts"

    shortcut_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    keystrokes: Mapped[list[str]] = mapped_column(JSON)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("shortcut_categories.category_id", ondelete="CASCADE")
    )
    category: Mapped["ShortcutCategory"] = relationship(back_populates="shortcuts")
