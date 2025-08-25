from __future__ import annotations
from dotenv import load_dotenv
from contextlib import contextmanager
from typing import Generator
from sqlmodel import SQLModel, create_engine, Session
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL, echo=True)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


@contextmanager
def session_context() -> Generator[Session, None, None]:
    with Session(engine) as s:
        yield s


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as s:
        yield s