import uuid
from datetime import datetime, timezone

from pydantic import conint

from enums.transaction_enum import TransactionStatus
from schemas.base_schema import BaseSchema


class TransactionRequest(BaseSchema):
    tuition_id: uuid.UUID


class TransactionCreate(TransactionRequest):
    status: TransactionStatus
    otp_secret: str
    otp_expiry_time: int
    user_id: uuid.UUID


class TransactionResponse(TransactionRequest):
    id: uuid.UUID
    is_paid: bool