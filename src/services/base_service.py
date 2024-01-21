import uuid
from math import ceil
from typing import Generic, TypeVar

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import asc, desc, func
from sqlalchemy.orm import Query, Session

from utils import set_value

SchemaCreateType = TypeVar("SchemaCreateType", bound=BaseModel)
SchemaUpdateType = TypeVar("SchemaUpdateType", bound=BaseModel)


class BaseService(Generic[SchemaCreateType, SchemaUpdateType]):
    def __init__(self, Model) -> None:
        self.Model = Model

    def create(self, session: Session, payload: SchemaCreateType):
        model = self.Model()
        set_value(model, payload)
        session.add(model)
        return model

    def get_by_id(self, session: Session, id: uuid.UUID):
        return session.query(self.Model).filter(self.Model.id == id).first()

    def update_by_id(self, session: Session, id: uuid.UUID, payload: SchemaUpdateType):
        model = self.get_by_id(session, id)
        set_value(model, payload)
        return

    def delete_by_id(self, session: Session, id: uuid.UUID):
        model = self.get_by_id(session, id)
        session.delete(model)
        return
