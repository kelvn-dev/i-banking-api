from enum import auto

from fastapi_restful.enums import StrEnum


class TransactionStatus(StrEnum):
    PENDING = auto()
    COMPLETED = auto()
    FAILED = auto()
    EXPIRED = auto()
