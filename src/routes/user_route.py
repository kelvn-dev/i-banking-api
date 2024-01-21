from fastapi import APIRouter, Depends, Request
from fastapi_utils.cbv import cbv

from security.user_session import UserSession, get_current_user

router = APIRouter(tags=["administrators"])
RESOURCE = "/administrators"


@cbv(router)
class AdministratorRouter:
    current_user: UserSession = Depends(get_current_user)

    @router.post(RESOURCE + "/invite")
    def invite(self):
        return self.current_user.user_info

    @router.get("/api/messages/protected")
    def protected(self):
        return {"text": "This is a protected message."}

    @router.get("/api/messages/admin")
    def admin(self):
        return {"text": "This is an admin message."}
