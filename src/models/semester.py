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


class Semester(BaseModel):
    __tablename__ = "semester"
    year = Column(SmallInteger(), nullable=False)
    code = Column(SmallInteger(), nullable=False)
