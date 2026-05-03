from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.prediction_schema import PredictionIn, PredictionOut
from app.services.ml_service import ml_service
from app.services.db_service import get_or_create_user, save_prediction
from app.utils.validators import clamp_percent

router = APIRouter(prefix="/predict", tags=["Predictions"])


@router.post("/", response_model=PredictionOut)
def predict(payload: PredictionIn, db: Session = Depends(get_db)):
    tenth = clamp_percent(payload.tenth_pct)
    twelfth = clamp_percent(payload.twelfth_pct)
    grad = clamp_percent(payload.graduation_pct)

    skills = payload.skills or []
    interest = payload.interest or ""
    city = payload.city or ""

    result = ml_service.predict(
        tenth_pct=tenth,
        twelfth_pct=twelfth,
        graduation_pct=grad,
        skills=skills,
        interest=interest,
        city=city
    )

    user_id = None
    if payload.full_name:
        user = get_or_create_user(db, full_name=payload.full_name, email=payload.email)
        user_id = user.id

    skills_csv = ",".join([s.strip() for s in skills if s and s.strip()]) if skills else None

    saved = save_prediction(
        db=db,
        user_id=user_id,
        tenth_pct=tenth,
        twelfth_pct=twelfth,
        graduation_pct=grad,
        skills_csv=skills_csv,
        interest=interest,
        city=city,
        predicted_career=result["predicted_career"],
        predicted_salary=result["predicted_salary"]
    )

    return PredictionOut(
        predicted_career=result["predicted_career"],
        predicted_salary=result["predicted_salary"],
        recommendation=result["recommendation"],
        roadmap=result["roadmap"],
        companies=result["companies"], 
        job_links=result["job_links"], 
        internships=result["internships"],
        courses=result["courses"],  
        saved_prediction_id=saved.id
    )