from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from app.core.config import settings
from app.api.routes import router
from app.models.database import init_db

app = FastAPI(title="Todo Telegram App API")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")

# Setup static files for photos
os.makedirs(settings.STATIC_DIR, exist_ok=True)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# Create symlink or copy structure for serving photos
photos_static_dir = os.path.join(settings.STATIC_DIR, "photos")
if not os.path.exists(photos_static_dir):
    os.makedirs(photos_static_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

@app.on_event("startup")
async def startup_event():
    init_db()
    print("Application started successfully!")

@app.get("/")
async def root():
    return {"message": "Todo Telegram App API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
