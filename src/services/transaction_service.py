import time
import uuid

from fastapi import HTTPException
from loguru import logger
from sqlalchemy import and_
from sqlalchemy.orm import Session

from enums.transaction_enum import TransactionStatus
from models import Transaction, User
from schemas.transaction_schema import TransactionCreate, TransactionRequest
from services.base_service import BaseService, SchemaCreateType
from services.provider import sendgrid_service
from utils.otp_utils import generate_otp_secret_key, generate_totp_code


class TransactionService(BaseService[TransactionRequest, TransactionRequest]):
    def validate_transaction_creation(
        self, session: Session, payload: TransactionRequest, user_id: uuid.UUID
    ):
        """
        Iterates through transactions with same tuition_id and raise exception if:
        - Transaction has been completed
        - Transaction requested by the same user hasn't expired yet
        """
        now = int(time.time())
        transactions = self.get_all_by_tuition_id(session, payload.tuition_id)

        for transaction in transactions:
            if transaction.status == TransactionStatus.COMPLETED:
                raise HTTPException(
                    status_code=409,
                    detail=f"Transaction has been completed for tuition id {payload.tuition_id} by user id {transaction.user_id} at {transaction.updated_time}",
                )
            if (
                transaction.user_id == user_id
                and transaction.tuition_id == payload.tuition_id
                and transaction.otp_expiry_time > now
            ):
                raise HTTPException(
                    status_code=409,
                    detail=f"Requested transaction hasn't expired yet. Please get otp in email to complete transaction",
                )

    def create(self, session: Session, payload: TransactionRequest, user: User):
        self.validate_transaction_creation(session, payload, user.id)
        otp_secret = generate_otp_secret_key()
        otp_code = generate_totp_code(otp_secret)
        # UNIX style timestamp representing 5 minutes from now
        otp_expiry_time = int(time.time() + 300)
        payload = TransactionCreate(
            tuition_id=payload.tuition_id,
            status=TransactionStatus.PENDING,
            otp_secret=otp_secret,
            otp_expiry_time=otp_expiry_time,
            user_id=user.id,
        )
        super().create(session, payload)
        sendgrid_service.send_otp_verification(user, otp_code)

    def get_all_by_tuition_id(
        self, session: Session, tuition_id: uuid.UUID
    ) -> list[Transaction]:
        transactions = (
            session.query(Transaction)
            .filter(Transaction.tuition_id == tuition_id)
            .all()
        )
        return transactions


transaction_service = TransactionService(Transaction)
