import time
import uuid

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload

from enums.transaction_enum import TransactionStatus
from models.transaction import Transaction
from models.tuition import Tuition
from models.user import User
from schemas.user_schema import UserUpdate
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

    def get_profile(self, session: Session, id: uuid.UUID):
        user = (
            session.query(User)
            .filter(User.id == id)
            .options(
                joinedload(User.transactions)
                .joinedload(Transaction.tuition)
                .joinedload(Tuition.student)
            )
            .first()
        )
        transactions: list[Transaction] = user.transactions
        now = int(time.time())
        for t in transactions:
            if t.status == TransactionStatus.PENDING and t.otp_expiry_time < now:
                t.status = TransactionStatus.EXPIRED
        return user

    def update_profile(self, session: Session, user: User, payload: UserUpdate):
        user_service.update_by_id(session, user.id, payload)
        # user.phone = payload.phone.
        # user.full_name = payload.full_name
        return


user_service = UserService(User)
