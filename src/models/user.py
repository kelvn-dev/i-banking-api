from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "app_user"
    auth0_user_id = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    full_name = Column(String(255))
    phone = Column(String(20))
    avatar = Column(String(255))
    balances = Column(Float(), nullable=False)
    transactions = relationship("Transaction", uselist=True)
