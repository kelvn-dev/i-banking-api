from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class Student(BaseModel):
    __tablename__ = "student"
    student_id = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
