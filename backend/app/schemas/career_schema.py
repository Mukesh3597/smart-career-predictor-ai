from pydantic import BaseModel

class CareerCreate(BaseModel):
    career_name: str
    min_salary: float = 0.0
    max_salary: float = 0.0

class CareerOut(BaseModel):
    id: int
    career_name: str
    min_salary: float
    max_salary: float

    class Config:
        from_attributes = True