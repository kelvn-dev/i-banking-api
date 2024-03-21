import uuid

from loguru import logger
from pydantic import BaseModel

from utils.time_utils import get_current_epoch


def set_value(model: object, data: BaseModel, exclude: set = {}):
    for key, value in data.model_dump(exclude=exclude, exclude_unset=True).items():
        if hasattr(model, key):
            setattr(model, key, value)
            logger.debug(f"{key}: {value}")
    return


def generate_random_string():
    id = str(uuid.uuid4())
    current_epoch = get_current_epoch()
    return f"{id.replace('-', '')}{current_epoch}"
