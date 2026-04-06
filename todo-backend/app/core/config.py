import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./todo.db")
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
    STATIC_DIR = os.getenv("STATIC_DIR", "./static")
    
settings = Settings()
