import time
from functools import wraps

from fastapi import Depends, HTTPException
from loguru import logger
from sqlalchemy import event
from sqlalchemy.orm import Session

from config.database import Base, get_session
from models import User
from schemas.user_schema import UserCreate
from security.auth0_oidc import Auth0Oidc
from services.provider import auth0_service
from services.rest.user_service import user_service

#########################################################################################
#
# Authentication
#
#########################################################################################


class UserSession:
    def __init__(self, user_info: User, session: Session, permissions: list[str]):
        self.user_info = user_info
        self.session = session
        self.permissions = permissions

        @event.listens_for(Base, "before_insert", propagate=True)
        def before_insert(mapper, connect, target):
            target.created_by = self.user_info.email
            target.created_time = int(time.time())

        @event.listens_for(Base, "before_update", propagate=True)
        def before_update(mapper, connect, target):
            target.updated_by = self.user_info.email
            target.updated_time = int(time.time())


auth0_oidc = Auth0Oidc()


async def get_current_user(
    payload=Depends(auth0_oidc.auth), session: Session = Depends(get_session)
):
    auth0_user_id = payload.get("sub")
    permissions = payload.get("permissions")
    user = user_service.get_by_auth0_user_id(session, auth0_user_id, False)
    if not user:
        auth0_user = auth0_service.get_by_id(auth0_user_id)
        logger.debug(auth0_user)
        user_schema = UserCreate(
            auth0_user_id=auth0_user_id,
            email=auth0_user.get("email"),
            balances=10_000_000,
        )
        user = user_service.create(session, user_schema)
    yield UserSession(user, session, permissions)


#########################################################################################
#
# Authorization
#
#########################################################################################


def authorize(required_permissions: list[str]):
    def decorator_auth(func):
        @wraps(func)
        def wrapper_auth(*args, **kwargs):
            self = kwargs["self"]
            current_user: UserSession = self.current_user

            token_permissions_set = set(current_user.permissions)
            required_permissions_set = set(required_permissions)
            if required_permissions_set.issubset(token_permissions_set):
                return func(*args, **kwargs)
            raise HTTPException(status_code=403, detail="Access denied")

        return wrapper_auth

    return decorator_auth
