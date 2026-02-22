from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Career(Base):
    __tablename__ = "careers"

    id = Column(Integer, primary_key=True, index=True)
    career_name = Column(String(120), unique=True, index=True, nullable=False)
    min_salary = Column(Float, default=0.0)
    max_salary = Column(Float, default=0.0)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)