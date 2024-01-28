import uuid
from datetime import datetime, timezone
from typing import Optional

from pydantic import conint

from enums.transaction_enum import TransactionStatus
from schemas.base_schema import BaseSchema
from schemas.tuition_schema import TuitionResponse


class TransactionRequest(BaseSchema):
    tuition_id: uuid.UUID


class TransactionCreate(TransactionRequest):
    status: TransactionStatus
    otp_secret: str
    otp_expiry_time: int
    user_id: uuid.UUID


class TransactionUpdate(BaseSchema):
    otp_code: str


class TransactionResponse(TransactionRequest):
    id: uuid.UUID
    user_id: uuid.UUID
    status: TransactionStatus
    tuition: TuitionResponse
    created_time: int
    updated_time: Optional[int]
