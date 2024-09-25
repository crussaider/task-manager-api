from fastapi import APIRouter, HTTPException
from app.models.db_models import User
from app.models.schemas import UserCreate, UserResponse

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@user_router.post("", response_model=UserResponse, status_code=201, response_description="User created")
async def create_user(user: UserCreate):
    """
    Создать нового пользователя.

    :param user: Схема создания пользователя с полями `username`, `email`, и `password`.

    :return: 201 Created: Возвращает созданного пользователя с полями `id`, `username`, и `email`.
    """
    db_user = User.create_user(username=user.username, email=user.email, password=user.password)
    return db_user


@user_router.get("/{user_id}", response_model=UserResponse, status_code=200, response_description="User read")
async def read_user(user_id: int):
    """
    Получить информацию о пользователе по его ID.

    :param user_id: Уникальный идентификатор пользователя.
    :return: 200 OK: Возвращает пользователя с полями `id`, `username`, и `email`.
    404 Not Found: Возвращает ошибку, если пользователь с указанным ID не найден.
    """
    db_user = await User.get_user(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


@user_router.put("/{user_id}", response_model=UserResponse, status_code=200, response_description="User updated")
async def update_user(user_id: int, user: UserCreate):
    """
    Обновить существующего пользователя по его ID.

    :param user_id: Уникальный идентификатор пользователя.
    :param user: Схема создания пользователя с новыми данными для обновления.
    :return: 200 OK: Возвращает обновленного пользователя с полями `id`, `username`, и `email`.
    404 Not Found: Возвращает ошибку, если пользователь с указанным ID не найден.
    """
    db_user = await User.update_user(user_id, username=user.username, email=user.email, password=user.password)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


@user_router.delete("/{user_id}", status_code=204, response_description="User deleted")
async def delete_user(user_id: int):
    """
    Удалить пользователя по его ID.

    :param user_id: Уникальный идентификатор пользователя.
    :return: 204 No Content: Указывает на успешное удаление пользователя.
    404 Not Found: Возвращает ошибку, если пользователь с указанным ID не найден.
    """
    db_user = await User.delete_user(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
