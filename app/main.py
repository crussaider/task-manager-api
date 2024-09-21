from fastapi import FastAPI
from app.config import fastapi_settings
from app.routers.user_router import user_router
from app.routers.task_router import task_router

app = FastAPI(
    title=fastapi_settings.app_title,
    description=fastapi_settings.app_description,
    contact=fastapi_settings.app_contacts,
    openapi_tags=fastapi_settings.tags_metadata,
)

app.include_router(user_router, prefix="/api/v1")
app.include_router(task_router, prefix="/api/v1")


@app.get("/", tags=["root"])
async def welcome_message():
    return {"message": "Welcome to Task Management System API"}
