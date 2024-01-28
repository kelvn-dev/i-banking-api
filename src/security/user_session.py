from datetime import datetime, timezone

from fastapi import Depends
from loguru import logger
from sqlalchemy import event
from sqlalchemy.orm import Session

from config.database import Base, get_session
from models import User
from schemas.user_schema import UserCreate
from security.auth0_oidc import Auth0Oidc
from services.provider import auth0_service
from services.user_service import user_service

#########################################################################################
#
# Authentication
#
#########################################################################################


class UserSession:
    def __init__(self, user_info, session):
        self.user_info: User = user_info
        self.session: Session = session

        @event.listens_for(Base, "before_insert", propagate=True)
        def before_insert(mapper, connect, target):
            target.created_by = self.user_info.email
            target.created_time = datetime.utcnow().replace(tzinfo=timezone.utc)

        @event.listens_for(Base, "before_update", propagate=True)
        def before_update(mapper, connect, target):
            target.updated_by = self.user_info.email
            target.updated_time = datetime.utcnow().replace(tzinfo=timezone.utc)


auth0_oidc = Auth0Oidc()


async def get_current_user(
    payload=Depends(auth0_oidc.auth), session: Session = Depends(get_session)
):
    auth0_user_id = payload["sub"]
    user = user_service.get_by_auth0_user_id(session, auth0_user_id, False)
    if not user:
        auth0_user = auth0_service.get_by_id(auth0_user_id)
        logger.debug(auth0_user)
        auth0_user_metadata = auth0_user["user_metadata"]
        user_schema = UserCreate(
            auth0_user_id=auth0_user_id,
            username=auth0_user["username"],
            email=auth0_user["email"],
            full_name=auth0_user_metadata["full_name"],
            phone=auth0_user_metadata["phone"],
            balances=10_000_000,
        )
        user = user_service.create(session, user_schema)
    yield UserSession(user, session)
