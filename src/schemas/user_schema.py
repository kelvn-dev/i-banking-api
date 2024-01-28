import uuid
from typing import Optional

from pydantic import EmailStr

from schemas.base_schema import BaseSchema
from schemas.transaction_schema import TransactionResponse


class UserCreate(BaseSchema):
    auth0_user_id: str
    email: EmailStr
    balances: float


class UserUpdate(BaseSchema):
    full_name: Optional[str]
    phone: Optional[str]


class UserProfile(BaseSchema):
    id: uuid.UUID
    email: EmailStr
    full_name: Optional[str]
    phone: Optional[str]
    balances: float
    transactions: list[TransactionResponse]
