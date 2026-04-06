import os
import uuid
import aiofiles
from datetime import datetime
from app.services.db_service import db
from app.core.config import settings

class PhotoService:
    async def upload_photo(self, file, user_id: int, task_id: int = None) -> dict:
        # Create user folder if not exists
        user_folder = os.path.join(settings.UPLOAD_DIR, str(user_id))
        os.makedirs(user_folder, exist_ok=True)
        
        # Generate unique filename
        file_extension = file.filename.split(".")[-1] if "." in file.filename else "jpg"
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        filepath = os.path.join(user_folder, unique_filename)
        
        # Save file
        async with aiofiles.open(filepath, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        
        # Save to database
        conn = await db.get_connection()
        cursor = await conn.cursor()
        
        now = datetime.now()
        await cursor.execute(
            "INSERT INTO photos (task_id, user_id, filename, filepath) VALUES (?, ?, ?, ?)",
            (task_id, user_id, unique_filename, filepath)
        )
        await conn.commit()
        
        photo_id = cursor.lastrowid
        await conn.close()
        
        # Return photo info with URL
        photo_url = f"/static/photos/{user_id}/{unique_filename}"
        
        return {
            "id": photo_id,
            "task_id": task_id,
            "filename": unique_filename,
            "url": photo_url,
            "user_id": user_id,
            "uploaded_at": now
        }
    
    async def get_photos_by_user(self, user_id: int) -> list[dict]:
        conn = await db.get_connection()
        cursor = await conn.cursor()
        
        await cursor.execute("SELECT * FROM photos WHERE user_id = ? ORDER BY uploaded_at DESC", (user_id,))
        rows = await cursor.fetchall()
        await conn.close()
        
        photos = []
        for row in rows:
            photos.append({
                "id": row["id"],
                "task_id": row["task_id"],
                "filename": row["filename"],
                "url": f"/static/photos/{user_id}/{row['filename']}",
                "user_id": row["user_id"],
                "uploaded_at": row["uploaded_at"]
            })
        
        return photos
    
    async def get_all_photos(self) -> list[dict]:
        conn = await db.get_connection()
        cursor = await conn.cursor()
        
        await cursor.execute("SELECT * FROM photos ORDER BY uploaded_at DESC")
        rows = await cursor.fetchall()
        await conn.close()
        
        photos = []
        for row in rows:
            photos.append({
                "id": row["id"],
                "task_id": row["task_id"],
                "filename": row["filename"],
                "url": f"/static/photos/{row['user_id']}/{row['filename']}",
                "user_id": row["user_id"],
                "uploaded_at": row["uploaded_at"]
            })
        
        return photos
