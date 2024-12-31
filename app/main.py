from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api import routers
from api.dependencies import create_db_and_tables

app = FastAPI()

app.include_router(routers.router)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")


@app.on_event('startup')
def on_startup():
    create_db_and_tables()
