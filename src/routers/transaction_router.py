from fastapi import Depends
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from schemas.transaction_schema import TransactionRequest
from security.user_session import UserSession, get_current_user
from services import transaction_service

router = InferringRouter(tags=["Transaction"])


@cbv(router)
class TransactionRouter:
    current_user: UserSession = Depends(get_current_user)

    @router.post("/transactions")
    def create(self, payload: TransactionRequest):
        transaction_service.create(
            self.current_user.session, payload, self.current_user.user_info.id
        )
        self.current_user.session.commit()
        return
