from fastapi import Depends
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from config.auth0_client import auth0_client
from schemas.user_schema import UserProfile
from security.user_session import UserSession, get_current_user
from services.user_service import user_service

router = InferringRouter(tags=["User"])


@cbv(router)
class UserRouter:
    current_user: UserSession = Depends(get_current_user)

    @router.get("/users/profile")
    def get_profile(self) -> UserProfile:
        self.current_user.session.commit()
        return self.current_user.user_info
