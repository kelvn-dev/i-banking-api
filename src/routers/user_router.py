from fastapi import Depends
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter
from loguru import logger

from config.auth0_client import auth0_client
from config.logto_client import client
from schemas.user_schema import UserProfile, UserUpdate
from security.user_session import UserSession, get_current_user
from services.user_service import user_service

router = InferringRouter(tags=["User"])


@cbv(router)
class UserRouter:
    current_user: UserSession = Depends(get_current_user)

    @router.get("/users/profile")
    def get_profile(self) -> UserProfile:
        self.current_user.session.commit()
        user = user_service.get_profile(
            self.current_user.session, self.current_user.user_info.id
        )
        return user

    @router.put("/users/profile")
    def update_profile(self, payload: UserUpdate):
        user_service.update_profile(
            self.current_user.session, self.current_user.user_info, payload
        )
        self.current_user.session.commit()
        return
