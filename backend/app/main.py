from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from app.config import APP_NAME
from app.database import Base, engine
from app.routes import user_router, career_router, prediction_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=APP_NAME)

# Static folder path
STATIC_DIR = Path(__file__).resolve().parents[1] / "static"   # backend/static

# Serve static files (css/js)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Homepage -> index.html
@app.get("/")
def serve_frontend():
    return FileResponse(str(STATIC_DIR / "index.html"))

# (Optional) CORS (safe to keep)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(user_router)
app.include_router(career_router)
app.include_router(prediction_router)