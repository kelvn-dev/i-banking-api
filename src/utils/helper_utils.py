from loguru import logger
from pydantic import BaseModel


def set_value(model: object, data: BaseModel, exclude: set = {}):
    for key, value in data.model_dump(exclude=exclude, exclude_unset=True).items():
        if hasattr(model, key):
            setattr(model, key, value)
            logger.debug(f"{key}: {value}")
    return
