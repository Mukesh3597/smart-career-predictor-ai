from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User")

    tenth_pct = Column(Float, nullable=False)
    twelfth_pct = Column(Float, nullable=False)
    graduation_pct = Column(Float, nullable=False)

    skills = Column(String(500), nullable=True)   # comma separated
    interest = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)

    predicted_career = Column(String(120), nullable=False)
    predicted_salary = Column(Float, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)