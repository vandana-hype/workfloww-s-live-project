
from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from app.dependencies import get_current_user
from app.schemas import TaskCreate, TaskStatusUpdate
from app.services.task_service import (
    create_task,
    get_tasks,
    update_task
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", status_code=201)
def create_new_task(
    task: TaskCreate,
    user=Depends(get_current_user)
):
    return create_task(user["supabase"], user, task)


@router.get("")
def retrieve_tasks(user=Depends(get_current_user)):
    return get_tasks(user["supabase"])


@router.patch("/{task_id}")
def change_task_status(
    task_id: UUID,
    task: TaskStatusUpdate,
    user=Depends(get_current_user)
):
    return update_task(user["supabase"], user, task_id, task)
