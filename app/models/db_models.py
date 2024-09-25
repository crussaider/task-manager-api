from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base
from dependencies import get_db, HASH_CONTEXT


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    @classmethod
    async def create_user(cls, username: str, email: str, password: str):
        db = get_db()
        db_user = User(username=username, email=email, hashed_password=HASH_CONTEXT.hash(password))

        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    @classmethod
    async def get_user(cls, user_id: int):
        db = get_db()
        db_user = await db.get(User, user_id)
        return db_user

    @classmethod
    async def update_user(cls, user_id: int, username: str, email: str, password: str):
        db = get_db()
        db_user = await cls.get_user(user_id)
        if not db_user:
            return db_user

        db_user.username = username
        db_user.email = email
        db_user.hashed_password = HASH_CONTEXT.hash(password)

        await db.commit()
        await db.refresh(db_user)
        return db_user

    @classmethod
    async def delete_user(cls, user_id: int):
        db = get_db()
        db_user = await cls.get_user(user_id)
        if not db_user:
            return db_user

        await db.delete(db_user)
        await db.commit()


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    is_completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User")

    @classmethod
    async def create_task(cls, title: str, description: str):
        db = await get_db()
        db_task = Task(title=title, description=description)

        db.add(db_task)
        await db.commit()
        await db.refresh(db_task)
        return db_task

    @classmethod
    async def get_task(cls, task_id: int):
        db = await get_db()
        db_task = await db.get(Task, task_id)
        return db_task

    @classmethod
    async def update_task(cls, task_id: int, title: str, description: str):
        db = await get_db()
        db_task = cls.get_task(task_id)
        if not db_task:
            return db_task

        db_task.title = title
        db_task.description = description

        await db.commit()
        await db.refresh(db_task)
        return db_task

    @classmethod
    async def delete_task(cls, task_id: int):
        db = await get_db()
        db_task = cls.get_task(task_id)
        if not db_task:
            return db_task

        await db.delete(db_task)
        await db.commit()
