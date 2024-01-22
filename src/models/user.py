from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "app_user"
    auth0_user_id = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    balances = Column(Float(), nullable=False)
