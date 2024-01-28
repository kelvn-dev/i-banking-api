import uuid

from enums.semester_enum import SemesterCode
from schemas.base_schema import BaseSchema


class StudentRequest(BaseSchema):
    student_id: str
    full_name: str


class TuitionResponse(BaseSchema):
    id: uuid.UUID
    is_paid: bool
    charges: float
    student_id: uuid.UUID
    semester_year: int
    semester_code: SemesterCode


class StudentResponse(StudentRequest):
    id: uuid.UUID
    tuition: list[TuitionResponse]
