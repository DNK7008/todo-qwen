from app.services.db_service import db
from app.schemas import TaskCreate, Task, TaskStatus
from datetime import datetime

class TaskService:
    async def create_task(self, task_data: TaskCreate, created_by: int) -> Task:
        conn = await db.get_connection()
        cursor = await conn.cursor()
        
        await cursor.execute(
            """INSERT INTO tasks (title, description, department, status, created_by, assigned_to) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            (task_data.title, task_data.description, task_data.department, 
             task_data.status.value, created_by, task_data.assigned_to)
        )
        await conn.commit()
        
        task_id = cursor.lastrowid
        now = datetime.now()
        
        await conn.close()
        
        return Task(
            id=task_id,
            title=task_data.title,
            description=task_data.description,
            department=task_data.department,
            status=task_data.status,
            created_by=created_by,
            assigned_to=task_data.assigned_to,
            created_at=now,
            updated_at=now
        )
    
    async def get_all_tasks(self) -> list[Task]:
        conn = await db.get_connection()
        cursor = await conn.cursor()
        
        await cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
        rows = await cursor.fetchall()
        await conn.close()
        
        tasks = []
        for row in rows:
            tasks.append(Task(
                id=row["id"],
                title=row["title"],
                description=row["description"],
                department=row["department"],
                status=TaskStatus(row["status"]),
                created_by=row["created_by"],
                assigned_to=row["assigned_to"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            ))
        
        return tasks
    
    async def get_tasks_by_department(self, department: str) -> list[Task]:
        conn = await db.get_connection()
        cursor = await conn.cursor()
        
        await cursor.execute("SELECT * FROM tasks WHERE department = ? ORDER BY created_at DESC", (department,))
        rows = await cursor.fetchall()
        await conn.close()
        
        tasks = []
        for row in rows:
            tasks.append(Task(
                id=row["id"],
                title=row["title"],
                description=row["description"],
                department=row["department"],
                status=TaskStatus(row["status"]),
                created_by=row["created_by"],
                assigned_to=row["assigned_to"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            ))
        
        return tasks
    
    async def update_task_status(self, task_id: int, status: TaskStatus) -> Task:
        conn = await db.get_connection()
        cursor = await conn.cursor()
        
        now = datetime.now()
        await cursor.execute(
            "UPDATE tasks SET status = ?, updated_at = ? WHERE id = ?",
            (status.value, now.isoformat(), task_id)
        )
        await conn.commit()
        
        await cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = await cursor.fetchone()
        await conn.close()
        
        if not row:
            return None
        
        return Task(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            department=row["department"],
            status=TaskStatus(row["status"]),
            created_by=row["created_by"],
            assigned_to=row["assigned_to"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )
