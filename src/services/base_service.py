import uuid
from typing import Generic, TypeVar

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from utils.helper_utils import set_value

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

    def get_by_id(self, session: Session, id: uuid.UUID, raise_exception=True):
        model = session.query(self.Model).filter(self.Model.id == id).first()
        if not model and raise_exception:
            raise HTTPException(
                status_code=404, detail=f"{self.Model.__name__} not found with id {id}"
            )
        return model

    def update_by_id(self, session: Session, id: uuid.UUID, payload: SchemaUpdateType):
        model = self.get_by_id(session, id)
        set_value(model, payload)
        return model

    def delete_by_id(self, session: Session, id: uuid.UUID):
        model = self.get_by_id(session, id)
        session.delete(model)
        return
