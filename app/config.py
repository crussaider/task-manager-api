from pydantic_settings import BaseSettings


class FastAPISettings(BaseSettings):
    app_title: str = "Task Manager"
    app_description: str = "Веб-приложение, которое предоставляет API для работы с системой управления задачами."
    app_contacts: dict = {
        "name": "Dmitry Ryapolov",
        "email": "dimaryapalov@gmail.com",
    }
    tags_metadata: list[dict] = [
        {
            "name": "root",
            "description": "Начальная страница.",
        },
    ]

    class Config:
        env_prefix = "FASTAPI_"


class DatabaseSettings(BaseSettings):
    __db_login: str = "postgres"
    __db_password: str = "password"
    __db_host: str = "localhost"
    __db_name: str = "task_management"
    db_url: str = f"postgresql://{__db_login}:{__db_password}@{__db_host}/{__db_name}"

    class Config:
        env_prefix = "DATABASE_"


fastapi_settings = FastAPISettings()
database_settings = DatabaseSettings()
