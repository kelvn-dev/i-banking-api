from fastapi_restful.guid_type import GUID
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from enums.transaction_enum import TransactionStatus
from models.base_model import BaseModel


class Transaction(BaseModel):
    __tablename__ = "app_transaction"
    status = Column(Enum(TransactionStatus), nullable=False)
    otp_secret = Column(String(255), nullable=False)
    otp_expiry_time = Column(Integer, nullable=False)
    user_id = Column(GUID, ForeignKey("app_user.id"))
    tuition_id = Column(GUID, ForeignKey("tuition.id"))
