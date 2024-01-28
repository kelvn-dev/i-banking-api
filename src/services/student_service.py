from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload

from models import Student
from models.base_model import BaseModel
from schemas.student_schema import StudentRequest
from services.base_service import BaseService, ModelType


class StudentService(BaseService[Student]):
    def create(self, session: Session, payload: StudentRequest):
        if self.get_by_student_id(session, payload.student_id, raise_exception=False):
            raise HTTPException(status_code=409)
        return super().create(session, payload)

    def get_by_student_id(
        self, session: Session, student_id: str, raise_exception=True
    ):
        student = (
            session.query(Student).filter(Student.student_id == student_id).first()
        )
        if not student and raise_exception:
            raise HTTPException(
                status_code=404,
                detail=f"{self.Model.__name__} not found with student id {student_id}",
            )
        return student

    def get_by_student_id_with_tuition(
        self, session: Session, student_id: str, raise_exception=True
    ):
        student = (
            session.query(Student)
            .filter(Student.student_id == student_id)
            .options(joinedload(Student.tuition))
            .first()
        )
        if not student and raise_exception:
            raise HTTPException(
                status_code=404,
                detail=f"{self.Model.__name__} not found with student id {student_id}",
            )
        return student


student_service = StudentService(Student)
