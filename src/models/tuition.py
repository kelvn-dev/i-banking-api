from fastapi_restful.guid_type import GUID
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class Tuition(BaseModel):
    __tablename__ = "tuition"
    charges = Column(Float(), nullable=False)
    semester_id = Column(GUID, ForeignKey("semester.id", ondelete="SET NULL"))
    semester = relationship("Semester")
