import uuid

from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session

from models import Tuition
from schemas.tuition_schema import TuitionRequest
from services import student_service
from services.base_service import BaseService, SchemaCreateType


class TuitionService(BaseService[Tuition, TuitionRequest, TuitionRequest]):
    def create(self, session: Session, payload: TuitionRequest):
        student_service.get_by_id(session, payload.student_id)
        if self.get_by_student_and_semester(
            session,
            student_id=payload.student_id,
            semester_year=payload.semester_year,
            semester_code=payload.semester_code,
            raise_exception=False,
        ):
            raise HTTPException(status_code=409)
        return super().create(session, payload)

    def get_by_student_and_semester(
        self,
        session: Session,
        student_id: uuid.UUID,
        semester_year: int,
        semester_code: int,
        raise_exception=True,
    ):
        tuition = (
            session.query(Tuition)
            .filter(
                and_(
                    Tuition.student_id == student_id,
                    Tuition.semester_year == semester_year,
                    Tuition.semester_code == semester_code,
                )
            )
            .first()
        )
        if not tuition and raise_exception:
            raise HTTPException(
                status_code=404,
                detail=f"{self.Model.__name__} not found with student id {student_id} and year {semester_year} and code {semester_code}",
            )
        return tuition

    def get_all_by_student_id(self, session: Session, student_id: uuid.UUID):
        tuition = session.query(Tuition).filter(Tuition.student_id == student_id).all()
        return tuition


tuition_service = TuitionService(Tuition)
