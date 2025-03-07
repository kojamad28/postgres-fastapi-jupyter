from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.dependencies import create_db_and_tables, DEBUG
from api.routers import base

app = FastAPI(debug=DEBUG)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

if DEBUG:
    app.include_router(
        base.router_dev,
        prefix="/api/user",
        tags=["Base"]
    )
else:
    app.include_router(
        base.router,
        prefix="/api/user",
        tags=["Base"]
    )


@app.on_event('startup')
def on_startup():
    create_db_and_tables()
