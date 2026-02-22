import os
from dotenv import load_dotenv

load_dotenv()

# Local dev के लिए SQLite default
# Deploy पर DATABASE_URL env में Postgres/MySQL दे देना
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./career_ai.db")

# ML artifacts folder (backend/ के relative)
ARTIFACT_DIR = os.getenv("ARTIFACT_DIR", "ml/artifacts")

APP_NAME = os.getenv("APP_NAME", "Smart Career Predictor AI")