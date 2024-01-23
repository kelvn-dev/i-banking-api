from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session

from enums.semester_enum import SemesterCode
from models import Semester
from schemas.semester_schema import SemesterRequest
from services.base_service import BaseService, SchemaCreateType


class SemesterService(BaseService[SemesterRequest, SemesterRequest]):
    def create(self, session: Session, payload: SemesterRequest):
        if self.get_by_year_and_code(session, payload.year, payload.code, False):
            raise HTTPException(status_code=409)
        return super().create(session, payload)

    def get_by_year_and_code(
        self, session: Session, year: int, code: SemesterCode, raise_exception=True
    ):
        semester = (
            session.query(Semester)
            .filter(and_(Semester.year == year, Semester.code == code.value))
            .first()
        )
        if not semester and raise_exception:
            raise HTTPException(
                status_code=404,
                detail=f"{self.Model.__name__} not found with year {year} and code {code}",
            )
        return semester


semester_service = SemesterService(Semester)
