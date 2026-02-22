from pydantic import BaseModel
from typing import Optional, List

class PredictionIn(BaseModel):
    # Optional user
    full_name: Optional[str] = None
    email: Optional[str] = None

    tenth_pct: float
    twelfth_pct: float
    graduation_pct: float

    skills: Optional[List[str]] = None
    interest: Optional[str] = None
    city: Optional[str] = None

class PredictionOut(BaseModel):
    predicted_career: str
    predicted_salary: float
    saved_prediction_id: int