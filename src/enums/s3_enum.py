from enum import auto

from fastapi_restful.enums import StrEnum


class ContentDisposition(StrEnum):
    INLINE = auto()
    ATTACHMENT = auto()
