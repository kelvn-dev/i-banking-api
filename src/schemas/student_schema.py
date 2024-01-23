import uuid

from schemas.base_schema import BaseSchema
from schemas.tuition_schema import TuitionResponse


class StudentRequest(BaseSchema):
    student_id: str
    full_name: str


class StudentResponse(StudentRequest):
    id: uuid.UUID


class StudentWithTuiTionResponse(StudentResponse):
    tuition: list[TuitionResponse]
