from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class AppUser(BaseModel):
    __tablename__ = "app_user"
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    auth0UserId = Column(String(255))
    is_verified = Column(Boolean, nullable=False)
