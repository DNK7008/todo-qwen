from app.services.db_service import db
from app.schemas import UserCreate, User

class UserService:
    async def get_or_create_user(self, telegram_id: int, phone: str, full_name: str, department: str = None) -> User:
        conn = await db.get_connection()
        cursor = await conn.cursor()
        
        # Try to find existing user
        await cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
        row = await cursor.fetchone()
        
        if row:
            await conn.close()
            return User(
                id=row["id"],
                telegram_id=row["telegram_id"],
                phone=row["phone"],
                full_name=row["full_name"],
                department=row["department"]
            )
        
        # Create new user
        await cursor.execute(
            "INSERT INTO users (telegram_id, phone, full_name, department) VALUES (?, ?, ?, ?)",
            (telegram_id, phone, full_name, department)
        )
        await conn.commit()
        
        user_id = cursor.lastrowid
        await conn.close()
        
        return User(
            id=user_id,
            telegram_id=telegram_id,
            phone=phone,
            full_name=full_name,
            department=department
        )
    
    async def get_user_by_id(self, user_id: int) -> User:
        conn = await db.get_connection()
        cursor = await conn.cursor()
        
        await cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = await cursor.fetchone()
        await conn.close()
        
        if not row:
            return None
        
        return User(
            id=row["id"],
            telegram_id=row["telegram_id"],
            phone=row["phone"],
            full_name=row["full_name"],
            department=row["department"]
        )
