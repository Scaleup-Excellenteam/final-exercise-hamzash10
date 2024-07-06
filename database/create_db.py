from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from sqlalchemy import create_engine, String, Integer, ForeignKey, DateTime, UUID
from typing import List
from datetime import datetime
import sys, os

DB_NAME = "mydatabase.db"
class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    # columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    # relations
    uploads: Mapped[List["Upload"]] = relationship("Upload", back_populates="user", cascade="all, delete, delete-orphan")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r})"


class Upload(Base):
    __tablename__ = 'uploads'

    # columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uid: Mapped[UUID] = mapped_column(UUID, unique=True, nullable=False)
    filename: Mapped[str] = mapped_column(String(50), nullable=False)
    upload_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    finish_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    # relations
    user: Mapped["User"] = relationship("User", back_populates="uploads")

    def __repr__(self) -> str:
        return f"Upload(id={self.id!r}, uid={self.uid!r}, filename={self.filename!r}, status={self.status!r})"



if not os.path.exists(DB_NAME):
    engine = create_engine(f"sqlite:///{DB_NAME}", echo=True)
    Base.metadata.create_all(bind=engine)

def get_session():
    Session = sessionmaker()
    return Session()


