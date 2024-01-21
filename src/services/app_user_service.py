from pydantic import BaseModel

from models.app_user import AppUser
from services.base_service import BaseService


class AppUserService(BaseService[BaseModel, BaseModel]):
    pass


app_user_service = AppUserService(AppUser)
