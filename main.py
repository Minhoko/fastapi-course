from fastapi import FastAPI

from config.settings import settings
from db.session import engine
from db.base import Base
from routers import users
from routers import jobs

import models


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_app():
    app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)
    create_tables()
    app.include_router(users.router)
    app.include_router(jobs.router)
    return app


app = start_app()


@app.get("/")
def read_root():
    return {"hello": "This is test"}
