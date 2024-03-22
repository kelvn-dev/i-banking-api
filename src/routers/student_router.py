from fastapi import Depends
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from schemas.student_schema import StudentRequest, StudentResponse
from security.user_session import UserSession, authorize, get_current_user
from services.rest.student_service import student_service

router = InferringRouter(tags=["Student"])


@cbv(router)
class StudentRouter:
    current_user: UserSession = Depends(get_current_user)

    @router.post("/students")
    @authorize(["write:students"])
    def create(self, payload: StudentRequest):
        student_service.create(self.current_user.session, payload)
        self.current_user.session.commit()
        return

    @router.get("/students/{student_id}")
    def get_by_student_id(self, student_id: str) -> StudentResponse:
        return student_service.get_by_student_id_with_tuition(
            self.current_user.session, student_id
        )
