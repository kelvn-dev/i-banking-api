import time
import uuid

from fastapi import HTTPException
from loguru import logger
from sqlalchemy import and_
from sqlalchemy.orm import Session

from enums.transaction_enum import TransactionStatus
from models import Transaction, User
from schemas.transaction_schema import (
    TransactionCreate,
    TransactionRequest,
    TransactionUpdate,
)
from services.base_service import BaseService
from services.provider import sendgrid_service
from services.student_service import student_service
from services.tuition_service import tuition_service
from utils.otp_utils import (
    generate_otp_secret_key,
    generate_totp_code,
    verify_totp_code,
)


class TransactionService(BaseService[Transaction]):
    def validate_transaction_creation(
        self, session: Session, tuition_id: uuid.UUID, user_id: uuid.UUID
    ):
        """
        Iterates through transactions with same tuition_id and raise exception if:
        - Transaction has been completed
        - Transaction requested by the same user hasn't expired yet
        """
        now = int(time.time())
        transactions = self.get_all_by_tuition_id(session, tuition_id)

        for transaction in transactions:
            if transaction.status == TransactionStatus.COMPLETED:
                raise HTTPException(
                    status_code=409,
                    detail=f"Transaction has been completed for tuition id {tuition_id} by user id {transaction.user_id} at {transaction.updated_time}",
                )
            if transaction.user_id == user_id and transaction.otp_expiry_time > now:
                raise HTTPException(
                    status_code=409,
                    detail=f"Requested transaction hasn't expired yet. Please get otp in email to complete transaction",
                )

    def validate_transaction_completion(self, session: Session, tuition_id: uuid.UUID):
        """
        Iterates through transactions with same tuition_id and raise exception if:
        - Transaction has been completed
        """
        transactions = self.get_all_by_tuition_id(session, tuition_id)

        for transaction in transactions:
            if transaction.status == TransactionStatus.COMPLETED:
                raise HTTPException(
                    status_code=409,
                    detail=f"Transaction has been completed for tuition id {tuition_id} by user id {transaction.user_id} at {transaction.updated_time}",
                )

    def create(self, session: Session, user: User, payload: TransactionRequest):
        tuition = tuition_service.get_by_id(session=session, id=payload.tuition_id)
        if user.balances < tuition.charges:
            raise HTTPException(status_code=400, detail="Insufficient balances")

        self.validate_transaction_creation(session, payload.tuition_id, user.id)
        otp_secret = generate_otp_secret_key()
        otp_code = generate_totp_code(otp_secret, 300)
        logger.debug(f"OTP: {otp_code}")
        # UNIX style timestamp representing 5 minutes from now
        otp_expiry_time = int(time.time() + 300)
        payload = TransactionCreate(
            tuition_id=payload.tuition_id,
            status=TransactionStatus.PENDING,
            otp_secret=otp_secret,
            otp_expiry_time=otp_expiry_time,
            user_id=user.id,
        )
        transaction = super().create(session, payload)
        sendgrid_service.send_otp_verification(user, otp_code)
        return transaction

    def get_all_by_tuition_id(
        self, session: Session, tuition_id: uuid.UUID
    ) -> list[Transaction]:
        transactions = (
            session.query(Transaction)
            .filter(Transaction.tuition_id == tuition_id)
            .all()
        )
        return transactions

    def update_by_id(
        self, session: Session, user: User, id: uuid.UUID, payload: TransactionUpdate
    ):
        transaction = self.get_by_id(session, id)
        if transaction.user_id != user.id:
            raise HTTPException(status_code=403, detail="Access denied")

        tuition = tuition_service.get_by_id(session, transaction.tuition_id)
        if user.balances < tuition.charges:
            raise HTTPException(status_code=400, detail="Insufficient balances")

        now = int(time.time())
        if transaction.otp_expiry_time < now:
            transaction.status = TransactionStatus.EXPIRED
            session.commit()
            raise HTTPException(status_code=403, detail="OTP has expired")

        if not verify_totp_code(transaction.otp_secret, 300, payload.otp_code):
            raise HTTPException(status_code=403, detail="Access denied")

        self.validate_transaction_completion(session, tuition_id=tuition.id)

        transaction.status = TransactionStatus.COMPLETED
        tuition.is_paid = True
        user.balances -= tuition.charges

        student = student_service.get_by_id(session, tuition.student_id)
        sendgrid_service.send_successful_payment_notification(
            user=user, student=student, tuition=tuition
        )

        return


transaction_service = TransactionService(Transaction)
