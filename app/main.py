from fastapi import FastAPI
from config import fastapi_settings

app = FastAPI(
    title=fastapi_settings.app_title,
    description=fastapi_settings.app_description,
    contact=fastapi_settings.app_contacts,
    openapi_tags=fastapi_settings.tags_metadata
)


@app.get("/", tags=["root"])
async def root():
    return {"message": "Welcome to Task Management System API"}
