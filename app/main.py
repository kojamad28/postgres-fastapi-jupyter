from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.dependencies import create_db_and_tables
from api.routers import user

app = FastAPI()

app.include_router(
    user.router,
    prefix="/api/user",
    tags=["user"]
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")


@app.on_event('startup')
def on_startup():
    create_db_and_tables()
