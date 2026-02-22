from sqlalchemy.orm import Session
from typing import Optional
from app.models import User, Prediction

def get_or_create_user(db: Session, full_name: str, email: Optional[str]):
    if email:
        user = db.query(User).filter(User.email == email).first()
        if user:
            return user
    user = User(full_name=full_name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def save_prediction(
    db: Session,
    user_id: Optional[int],
    tenth_pct: float,
    twelfth_pct: float,
    graduation_pct: float,
    skills_csv: Optional[str],
    interest: Optional[str],
    city: Optional[str],
    predicted_career: str,
    predicted_salary: float
):
    pred = Prediction(
        user_id=user_id,
        tenth_pct=tenth_pct,
        twelfth_pct=twelfth_pct,
        graduation_pct=graduation_pct,
        skills=skills_csv,
        interest=interest,
        city=city,
        predicted_career=predicted_career,
        predicted_salary=predicted_salary
    )
    db.add(pred)
    db.commit()
    db.refresh(pred)
    return pred