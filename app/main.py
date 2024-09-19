from fastapi import FastAPI
from config import FASTAPI

app = FastAPI(
    title=FASTAPI.APP_TITLE,
    description=FASTAPI.APP_DESCRIPTION,
    contact=FASTAPI.APP_CONTACTS,
    openapi_tags=FASTAPI.TAGS_METADATA
)


@app.get("/", tags=["root"])
async def root():
    return {"message": "Welcome to Task Management System API"}
