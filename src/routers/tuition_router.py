from fastapi import Depends
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from schemas.tuition_schema import TuitionRequest
from security.user_session import UserSession, authorize, get_current_user
from services.rest.tuition_service import tuition_service

router = InferringRouter(tags=["Tuition"])


@cbv(router)
class TuitionRouter:
    current_user: UserSession = Depends(get_current_user)

    @router.post("/tuition")
    @authorize(["write:tuition"])
    def create(self, payload: TuitionRequest):
        tuition_service.create(self.current_user.session, payload)
        self.current_user.session.commit()
        return
