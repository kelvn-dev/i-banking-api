from fastapi import Depends
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from config.auth0_client import auth0_client
from enums.semester_enum import SemesterCode
from schemas.semester_schema import SemesterRequest
from security.user_session import UserSession, get_current_user
from services import semester_service

router = InferringRouter(tags=["Semester"])


@cbv(router)
class SemesterRouter:
    current_user: UserSession = Depends(get_current_user)

    @router.post("/semesters")
    def create(self, payload: SemesterRequest):
        semester_service.create(self.current_user.session, payload)
        self.current_user.session.commit()
        return
