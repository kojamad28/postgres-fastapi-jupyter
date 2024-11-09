from dotenv import dotenv_values
from sqlalchemy import URL
from sqlmodel import SQLModel, Session, create_engine


config = dotenv_values("api/.env.development")
#config = dotenv_values("api/.env")


DEBUG = config.get("DEBUG", "false").lower() == "true"


db_url = URL.create(
        "postgresql+psycopg",
        username=config["DATABASE_USER"],
        password=config["DATABASE_PASSWORD"],  # plain (unescaped) text
        host=config["DATABASE_HOST"],
        port=config["DATABASE_PORT"],
        database=config["DATABASE_DB"],
        query={"options": f"-c search_path={config['DATABASE_SCHEMA']}"},
)
connect_args = {}
engine = create_engine(db_url, echo=DEBUG, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
