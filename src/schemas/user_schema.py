import uuid

from pydantic import EmailStr

from schemas.base_schema import BaseSchema


class UserCreate(BaseSchema):
    auth0_user_id: str
    username: str
    email: EmailStr
    full_name: str
    phone: str
    balances: float


class UserProfile(BaseSchema):
    id: uuid.UUID
    username: str
    email: EmailStr
    full_name: str
    phone: str
    balances: float
