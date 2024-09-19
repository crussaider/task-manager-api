from pydantic import BaseSettings


class FastAPISettings(BaseSettings):
    app_title: str = "Task Manager"
    app_description: str = "Веб-приложение, которое предоставляет API для работы с системой управления задачами."
    app_contacts: dict = {
        "name": "Dmitry Ryapolov",
        "email": "dimaryapalov@gmail.com",
    }
    tags_metadata: list = [
        {
            "name": "root",
            "description": "Начальная страница.",
        },
    ]

    class Config:
        env_prefix = "FASTAPI_"  # Префикс для переменных окружения


fastapi_settings = FastAPISettings()
