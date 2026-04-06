import aiosqlite
from app.core.config import settings

class Database:
    def __init__(self):
        self.db_url = settings.DATABASE_URL
    
    async def get_connection(self) -> aiosqlite.Connection:
        conn = await aiosqlite.connect(self.db_url.replace("sqlite+aiosqlite://", ""))
        conn.row_factory = aiosqlite.Row
        return conn

db = Database()
