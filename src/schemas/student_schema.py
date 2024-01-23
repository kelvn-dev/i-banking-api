import uuid

from schemas.base_schema import BaseSchema


class StudentRequest(BaseSchema):
    student_id: str
    full_name: str


class StudentResponse(StudentRequest):
    pass
