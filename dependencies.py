from app.db.database import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

# Хеширование пароля
HASH_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_db() -> AsyncSession:
    """
    Зависимость для получения сеанса базы данных SQLAlchemy.

    :return: Экземпляр сеанса SQLAlchemy.
    """
    async with SessionLocal() as session:
        yield session
