from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from models.user import User
from services.base_service import BaseService


class UserService(BaseService[User]):
    def get_by_auth0_user_id(
        self, session: Session, auth0_user_id: str, raise_exception=True
    ):
        user = session.query(User).filter(User.auth0_user_id == auth0_user_id).first()
        if not user and raise_exception:
            raise HTTPException(
                status_code=404,
                detail=f"{self.Model.__name__} not found with auth0UserId {auth0_user_id}",
            )
        return user


user_service = UserService(User)
