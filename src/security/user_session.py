from datetime import datetime, timezone
from functools import wraps

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import event
from sqlalchemy.orm import Session

from security.auth0_oidc import Auth0Oidc

# from database import Base, get_session
# from models import AppUser, Group
# from services import app_user_service
# from utils import decode_token

#########################################################################################
#
# Authentication
#
#########################################################################################


class UserSession:
    def __init__(self, user_info, session):
        self.user_info = user_info
        # self.session: Session = session

        # @event.listens_for(Base, 'before_insert', propagate=True)
        # def before_insert(mapper, connect, target):
        #     target.created_by = self.user_info.email
        #     target.created_time = datetime.utcnow().replace(tzinfo=timezone.utc)
        #
        # @event.listens_for(Base, 'before_update', propagate=True)
        # def before_update(mapper, connect, target):
        #     target.updated_by = self.user_info.email
        #     target.updated_time = datetime.utcnow().replace(tzinfo=timezone.utc)


auth_scheme = HTTPBearer()
auth0_oidc = Auth0Oidc()


async def get_current_user(payload=Depends(auth0_oidc.auth)):
    yield UserSession(payload, payload)
    # app_user = app_user_service.get_by_id_with_group(session, payload['sub'])
    # yield UserSession(app_user, session)
