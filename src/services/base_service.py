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

    def get_query(self, session: Session, condition: list = []):
        query = session.query(self.Model).filter(*condition)
        return query

    def get_list(self, query: Query, params: ListingParams):
        total_items: int = query.distinct().count()
        total_pages: int = ceil(total_items / params.page_size)

        direction = asc if params.order == "asc" else desc
        # Cannot sort case insensitive with datetime, uuid, integer,...
        list_case_sensitive = ["DATETIME", "DATE", "CHAR(32)", "INTEGER"]
        try:
            column = getattr(self.Model, params.sort_by)
            if str(column.type) in list_case_sensitive:
                criterion = direction(column)
            else:
                criterion = direction(func.lower(column))
            items = (
                query.order_by(criterion)
                .limit(params.page_size)
                .offset(params.page_index * params.page_size)
                .all()
            )
        except:
            raise HTTPException(
                status_code=501, detail=f"Unable to sort by column {params.sort_by}"
            )

        return {
            "items": jsonable_encoder(items),
            "total_items": total_items,
            "total_pages": total_pages,
        }
