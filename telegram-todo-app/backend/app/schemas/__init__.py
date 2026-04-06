from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class UserBase(BaseModel):
    telegram_id: int
    phone: str
    full_name: str
    department: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    
    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    department: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING

class TaskCreate(TaskBase):
    assigned_to: Optional[int] = None

class Task(TaskBase):
    id: int
    created_by: int
    assigned_to: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class PhotoUpload(BaseModel):
    task_id: Optional[int] = None
    filename: str
    filepath: str
    uploaded_at: datetime
    
    class Config:
        from_attributes = True

class PhotoResponse(BaseModel):
    id: int
    task_id: Optional[int]
    filename: str
    url: str
    user_id: int
    uploaded_at: datetime
    
    class Config:
        from_attributes = True
