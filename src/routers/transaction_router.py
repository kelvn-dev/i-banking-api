import uuid

from fastapi import Depends
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from schemas.transaction_schema import (
    TransactionRequest,
    TransactionResponse,
    TransactionUpdate,
)
from security.user_session import UserSession, get_current_user
from services.transaction_service import transaction_service

router = InferringRouter(tags=["Transaction"])


@cbv(router)
class TransactionRouter:
    current_user: UserSession = Depends(get_current_user)

    @router.post("/transactions")
    def create(self, payload: TransactionRequest) -> TransactionResponse:
        transaction = transaction_service.create(
            session=self.current_user.session,
            user=self.current_user.user_info,
            payload=payload,
        )
        return transaction

    @router.put("/transactions/{id}")
    def update_by_id(self, id: uuid.UUID, payload: TransactionUpdate):
        transaction_service.update_by_id(
            session=self.current_user.session,
            user_id=self.current_user.user_info.id,
            id=id,
            payload=payload,
        )
        return
