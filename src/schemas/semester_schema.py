import uuid

from pydantic import conint

from enums.semester_enum import SemesterCode
from schemas.base_schema import BaseSchema


class SemesterRequest(BaseSchema):
    year: conint(ge=1997, le=2030)
    code: SemesterCode
