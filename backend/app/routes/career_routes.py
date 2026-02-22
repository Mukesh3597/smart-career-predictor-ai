from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.career_schema import CareerCreate, CareerOut
from app.models import Career

router = APIRouter(prefix="/careers", tags=["Careers"])

@router.post("/", response_model=CareerOut)
def create_career(payload: CareerCreate, db: Session = Depends(get_db)):
    c = Career(career_name=payload.career_name, min_salary=payload.min_salary, max_salary=payload.max_salary)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

@router.get("/", response_model=list[CareerOut])
def list_careers(db: Session = Depends(get_db)):
    return db.query(Career).order_by(Career.career_name.asc()).all()