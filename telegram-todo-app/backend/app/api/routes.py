from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from app.services.user_service import UserService
from app.services.task_service import TaskService
from app.services.photo_service import PhotoService
from app.schemas import UserCreate, TaskCreate, TaskStatus
from typing import List

router = APIRouter()

user_service = UserService()
task_service = TaskService()
photo_service = PhotoService()

def get_current_user(telegram_id: int = Form(...), phone: str = Form(...), full_name: str = Form(...), department: str = Form(None)):
    return user_service.get_or_create_user(telegram_id, phone, full_name, department)

@router.post("/auth")
async def auth_user(
    telegram_id: int = Form(...),
    phone: str = Form(...),
    full_name: str = Form(...),
    department: str = Form(None)
):
    user = await user_service.get_or_create_user(telegram_id, phone, full_name, department)
    return {"user": user}

@router.get("/tasks", response_model=List[dict])
async def get_tasks(department: str = None):
    if department:
        tasks = await task_service.get_tasks_by_department(department)
    else:
        tasks = await task_service.get_all_tasks()
    return {"tasks": tasks}

@router.post("/tasks")
async def create_task(
    title: str = Form(...),
    description: str = Form(None),
    department: str = Form(None),
    status: str = Form("pending"),
    assigned_to: int = Form(None),
    telegram_id: int = Form(...)
):
    user = await user_service.get_user_by_id(telegram_id)  # Simplified for demo
    if not user:
        # Create temp user for demo
        user = await user_service.get_or_create_user(telegram_id, "+000000000", "Demo User", department)
    
    task_data = TaskCreate(
        title=title,
        description=description,
        department=department,
        status=TaskStatus(status),
        assigned_to=assigned_to
    )
    
    task = await task_service.create_task(task_data, user.id)
    return {"task": task}

@router.put("/tasks/{task_id}/status")
async def update_task_status(task_id: int, status: str = Form(...)):
    task = await task_service.update_task_status(task_id, TaskStatus(status))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task": task}

@router.post("/photos/upload")
async def upload_photo(
    file: UploadFile = File(...),
    user_id: int = Form(...),
    task_id: int = Form(None)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    photo = await photo_service.upload_photo(file, user_id, task_id)
    return {"photo": photo}

@router.get("/photos", response_model=List[dict])
async def get_photos(user_id: int = None):
    if user_id:
        photos = await photo_service.get_photos_by_user(user_id)
    else:
        photos = await photo_service.get_all_photos()
    return {"photos": photos}
