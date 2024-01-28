import uuid
from typing import Optional

from pydantic import EmailStr

from enums.semester_enum import SemesterCode
from enums.transaction_enum import TransactionStatus
from schemas.base_schema import BaseSchema


class UserCreate(BaseSchema):
    auth0_user_id: str
    email: EmailStr
    balances: float


class UserUpdate(BaseSchema):
    full_name: str = None
    phone: str = None


class StudentResponse(BaseSchema):
    id: uuid.UUID
    student_id: str
    full_name: str


class TuitionResponse(BaseSchema):
    id: uuid.UUID
    charges: float
    semester_year: int
    semester_code: SemesterCode
    is_paid: bool
    student_id: uuid.UUID
    student: StudentResponse


class TransactionResponse(BaseSchema):
    id: uuid.UUID
    user_id: uuid.UUID
    status: TransactionStatus
    tuition: TuitionResponse
    created_time: int
    updated_time: Optional[int]


class UserProfile(BaseSchema):
    id: uuid.UUID
    email: EmailStr
    full_name: Optional[str]
    phone: Optional[str]
    balances: float
    transactions: list[TransactionResponse]
