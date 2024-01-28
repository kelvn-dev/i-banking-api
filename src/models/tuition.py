from fastapi_restful.guid_type import GUID
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    SmallInteger,
    String,
)
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class Tuition(BaseModel):
    __tablename__ = "tuition"
    charges = Column(Float(), nullable=False)
    is_paid = Column(Boolean(), default=False)
    semester_year = Column(SmallInteger(), nullable=False)
    semester_code = Column(SmallInteger(), nullable=False)
    student_id = Column(GUID, ForeignKey("student.id", ondelete="SET NULL"))
    student = relationship("Student", uselist=False)
