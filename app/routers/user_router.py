from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db_models import User
from app.models.schemas import UserCreate, UserResponse
from passlib.context import CryptContext
from dependencies import get_db

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
)

# Хеширование пароля
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@user_router.post("", response_model=UserResponse, status_code=201, response_description="User created")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Создать нового пользователя.

    :param user: Схема создания пользователя с полями `username`, `email`, и `password`.
    :param db: Асинхронная сессия SQLAlchemy для взаимодействия с базой данных (автоматически предоставляется через Depends).

    :return: 201 Created: Возвращает созданного пользователя с полями `id`, `username`, и `email`.
    """
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


@user_router.get("/{user_id}", response_model=UserResponse, status_code=200, response_description="User read")
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Получить информацию о пользователе по его ID.

    :param user_id: Уникальный идентификатор пользователя.
    :param db: Асинхронная сессия SQLAlchemy для взаимодействия с базой данных (автоматически предоставляется через Depends).
    :return: 200 OK: Возвращает пользователя с полями `id`, `username`, и `email`.
    404 Not Found: Возвращает ошибку, если пользователь с указанным ID не найден.
    """
    db_user = await db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


@user_router.put("/{user_id}", response_model=UserResponse, status_code=200, response_description="User updated")
async def update_user(user_id: int, user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Обновить существующего пользователя по его ID.

    :param user_id: Уникальный идентификатор пользователя.
    :param user: Схема создания пользователя с новыми данными для обновления.
    :param db: Асинхронная сессия SQLAlchemy для взаимодействия с базой данных (автоматически предоставляется через Depends).
    :return: 200 OK: Возвращает обновленного пользователя с полями `id`, `username`, и `email`.
    404 Not Found: Возвращает ошибку, если пользователь с указанным ID не найден.
    """
    db_user = await db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.username = user.username
    db_user.email = user.email
    db_user.hashed_password = pwd_context.hash(user.password)
    await db.commit()
    await db.refresh(db_user)
    return db_user


@user_router.delete("/{user_id}", status_code=204, response_description="User deleted")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Удалить пользователя по его ID.

    :param user_id: Уникальный идентификатор пользователя.
    :param db: Асинхронная сессия SQLAlchemy для взаимодействия с базой данных (автоматически предоставляется через Depends).
    :return: 204 No Content: Указывает на успешное удаление пользователя.
    404 Not Found: Возвращает ошибку, если пользователь с указанным ID не найден.
    """
    db_user = await db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(db_user)
    await db.commit()
