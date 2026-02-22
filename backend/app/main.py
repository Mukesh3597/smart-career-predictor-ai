from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from app.config import APP_NAME
from app.routes import user_router, career_router, prediction_router
from app.database import init_db  # ✅ safe init

app = FastAPI(title=APP_NAME)

# ✅ Init DB safely on startup (won't crash if already exists)
@app.on_event("startup")
def on_startup():
    init_db()

# Static folder path: backend/static
STATIC_DIR = Path(__file__).resolve().parents[1] / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse(str(STATIC_DIR / "index.html"))

# Optional: CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(user_router)
app.include_router(career_router)
app.include_router(prediction_router)