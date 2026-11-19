
from pydantic import BaseModel, Field
from typing import Literal, Optional
from uuid import UUID


TaskStatus = Literal["pending", "in_progress", "completed"]


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    description: Optional[str] = None
    assigned_to: UUID


class TaskStatusUpdate(BaseModel):
    status: TaskStatus
