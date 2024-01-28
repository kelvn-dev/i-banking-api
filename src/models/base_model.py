from fastapi_restful.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from sqlalchemy import Column, DateTime, Integer, String

from config.database import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(GUID, primary_key=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    created_by = Column(String, nullable=False)
    created_time = Column(Integer, nullable=False)
    updated_by = Column(String)
    updated_time = Column(Integer)
