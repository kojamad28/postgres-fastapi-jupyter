import os
from pathlib import Path

from sqlmodel import SQLModel

from db.session import get_engine, get_sessionlocal

BASE_DIR = Path(__file__).resolve().parent.parent


def read_boolean(value: str) -> bool:
    return value.lower() in ('true', 't', 'yes', 'y', 'on', '1')

DEBUG = read_boolean(str(os.environ.get("DEBUG", "False")))

if DEBUG:
    DOTENV_PATH = BASE_DIR / "db" / ".env.dev"
else:
    DOTENV_PATH = BASE_DIR / "db" / ".env"


def create_db_and_tables():
    engine = get_engine(DOTENV_PATH)
    SQLModel.metadata.create_all(engine)


async def get_session(dotenv_path: str = DOTENV_PATH):
    session = get_sessionlocal(dotenv_path)()
    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()
