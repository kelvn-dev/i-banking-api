from fastapi import Depends
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from schemas.student_schema import StudentRequest
from security.user_session import UserSession, get_current_user
from services import student_service

router = InferringRouter(tags=["Student"])


@cbv(router)
class StudentRouter:
    current_user: UserSession = Depends(get_current_user)

    @router.post("/students")
    def create(self, payload: StudentRequest):
        student_service.create(self.current_user.session, payload)
        self.current_user.session.commit()
        return
