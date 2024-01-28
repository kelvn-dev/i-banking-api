from loguru import logger

from schemas.base_schema import BaseSchema


def is_pydantic(obj: object):
    """Checks whether an object is pydantic."""
    return type(obj).__class__.__name__ == "ModelMetaclass"


def pydantic_to_sqlalchemy_model(schema: BaseSchema):
    """
    Iterates through pydantic schema and parses nested schemas
    to a dictionary containing SQLAlchemy models.
    Only works if nested schemas have specified the Meta.orm_model.
    """
    parsed_schema = schema.model_dump(exclude_unset=True, exclude_none=True)
    logger.debug(parsed_schema)
    for key, value in parsed_schema.items():
        try:
            if isinstance(value, list) and len(value) and is_pydantic(value[0]):
                parsed_schema[key] = [
                    item.Meta.orm_model(**pydantic_to_sqlalchemy_model(item))
                    for item in value
                ]
            elif is_pydantic(value):
                parsed_schema[key] = value.Meta.orm_model(
                    **pydantic_to_sqlalchemy_model(value)
                )
        except AttributeError:
            raise AttributeError(
                f"Found nested Pydantic model in {schema.__class__} but Meta.orm_model was not specified."
            )
    return parsed_schema
