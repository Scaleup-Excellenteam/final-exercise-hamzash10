from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DateTime
from typing import List
from uuid import UUID
from datetime import datetime
import sys, os


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    # columns
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    # relations
    uploads: Mapped[List["Upload"]] = relationship(back_populates="user", cascade="all, delete, delete-orphan")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r})"


class Upload(Base):
    __tablename__ = 'uploads'

    # columns
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uid: Mapped[UUID] = mapped_column(unique=True, nullable=False)
    filename: Mapped[str] = mapped_column(nullable=False)
    upload_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    finish_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # relations
    user: Mapped["User"] = relationship(back_populates="uploads")

    def __repr__(self) -> str:
        return f"Upload(id={self.id!r}, uid={self.uid!r}, filename={self.filename!r}, status={self.status!r})"


db_path = os.path.join(os.path.dirname(__file__), "mydatabase.db")

if not os.path.exists(db_path):
    os.makedirs(db_path)



if not os.path.exists(db_path):
    engine = create_engine(f"sqlite:///{db_path}", echo=True)
    Base.metadata.create_all(engine)

def get_session():
    Session = sessionmaker(bind=engine)
    return Session()


