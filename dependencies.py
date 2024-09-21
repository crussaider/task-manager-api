from app.db.database import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db() -> AsyncSession:
    """
    Зависимость для получения сеанса базы данных SQLAlchemy.

    :return: Экземпляр сеанса SQLAlchemy.
    """
    async with SessionLocal() as session:
        yield session
