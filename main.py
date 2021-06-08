from fastapi import FastAPI

from config.settings import settings

app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)


@app.get("/")
def read_root():
    return {"hello": "This is test"}
