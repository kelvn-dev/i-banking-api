import uuid

from pydantic import conint

from enums.semester_enum import SemesterCode
from schemas.base_schema import BaseSchema


class TuitionRequest(BaseSchema):
    charges: float
    student_id: uuid.UUID
    semester_year: conint(ge=1997, le=2030)
    semester_code: SemesterCode


class StudentResponse(BaseSchema):
    id: uuid.UUID
    student_id: str
    full_name: str


class TuitionResponse(TuitionRequest):
    id: uuid.UUID
    is_paid: bool
    student: StudentResponse
