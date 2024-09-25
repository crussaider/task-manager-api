from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db_models import Task
from app.models.schemas import TaskCreate, TaskResponse
from dependencies import get_db

task_router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@task_router.post("", response_model=TaskResponse, status_code=201, response_description="User created")
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    """
    Создать новую задачу.

    :param task: Схема задачи, которая содержит поля `title` и `description`.
    :param db: Асинхронная сессия SQLAlchemy для взаимодействия с базой данных (автоматически предоставляется через Depends).

    :return: 201 Created: Возвращает созданную задачу с полями `id`, `title`, и `description`.
    """
    db_task = await Task.create_task(db, task.title, task.description)
    return db_task


@task_router.get("/{task_id}", response_model=TaskResponse, status_code=200, response_description="User read")
async def read_task(task_id: int, db: AsyncSession = Depends(get_db)):
    """
    Получить информацию о задаче по её ID.

    :param task_id: Уникальный идентификатор задачи.
    :param db: Асинхронная сессия SQLAlchemy для взаимодействия с базой данных (автоматически предоставляется через Depends).
    :return: 200 OK: Возвращает задачу с полями `id`, `title`, и `description`, если задача найдена.
    404 Not Found: Возвращает ошибку, если задача с указанным ID не найдена.
    """
    db_task = await Task.get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return db_task


@task_router.put("/{task_id}", response_model=TaskResponse, status_code=200, response_description="User updated")
async def update_task(task_id: int, task: TaskCreate, db: AsyncSession = Depends(get_db)):
    """
    Обновить существующую задачу по её ID.

    :param task_id: Уникальный идентификатор задачи.
    :param task: Схема задачи с новыми данными для обновления.
    :param db: Асинхронная сессия SQLAlchemy для взаимодействия с базой данных (автоматически предоставляется через Depends).
    :return: 200 OK: Возвращает обновлённую задачу с полями `id`, `title`, и `description`.
    404 Not Found: Возвращает ошибку, если задача с указанным ID не найдена.
    """
    db_task = await Task.update_task(db, task_id, title=task.title, description=task.description)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return db_task


@task_router.delete("/{task_id}", status_code=204, response_description="Task deleted")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    """
    Удалить задачу по её ID.

    :param task_id: Уникальный идентификатор задачи.
    :param db: Асинхронная сессия SQLAlchemy для взаимодействия с базой данных (автоматически предоставляется через Depends).
    :return: 204 No Content: Указывает на успешное удаление задачи.
    404 Not Found: Возвращает ошибку, если задача с указанным ID не найдена.
    """
    result = await Task.delete_task(db, task_id)
    if result == 0:
        return
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
