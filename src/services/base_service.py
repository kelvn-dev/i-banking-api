import uuid
from typing import Generic, TypeVar

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from models.base_model import BaseModel
from utils.helper_utils import set_value
from utils.mapping_utils import pydantic_to_sqlalchemy_model

ModelType = TypeVar("ModelType", bound=BaseModel)
SchemaCreateType = TypeVar("SchemaCreateType", bound=BaseModel)
SchemaUpdateType = TypeVar("SchemaUpdateType", bound=BaseModel)


class BaseService(Generic[ModelType, SchemaCreateType, SchemaUpdateType]):
    def __init__(self, Model) -> None:
        self.Model = Model

    def create(self, session: Session, payload: SchemaCreateType) -> ModelType:
        model = self.Model(**pydantic_to_sqlalchemy_model(payload))
        # set_value(model, payload)
        session.add(model)
        return model

    def get_by_id(
        self, session: Session, id: uuid.UUID, raise_exception=True
    ) -> ModelType:
        model = session.query(self.Model).filter(self.Model.id == id).first()
        if not model and raise_exception:
            raise HTTPException(
                status_code=404, detail=f"{self.Model.__name__} not found with id {id}"
            )
        return model

    def update_by_id(self, session: Session, id: uuid.UUID, payload: SchemaUpdateType):
        # model = self.get_by_id(session, id)
        # set_value(model, payload)
        session.query(ModelType).filter(ModelType.id == id).update(
            **pydantic_to_sqlalchemy_model(payload)
        )
        return

    def delete_by_id(self, session: Session, id: uuid.UUID):
        model = self.get_by_id(session, id)
        session.delete(model)
        return
