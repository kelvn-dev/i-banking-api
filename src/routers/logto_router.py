import requests
from fastapi import Depends
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter
from loguru import logger

from config.logto_client import client

router = InferringRouter(tags=["Logto"], prefix="/logto")


@cbv(router)
class LogtoRouter:
    @router.get("/users")
    async def get_users(self):
        response = requests.post(
            "http://localhost:3001/oidc/token",
            headers={
                "Authorization": "Basic dXlieTJ5Zmg0cmhydTd0NHp0Zm54Om50R0tuNmdvbm5veXY1amZEUjVTMEVLM0dQUGgxZHJn"
            },
            data={
                "grant_type": "client_credentials",
                "resource": "https://default.logto.app/api",
                "scope": "all",
            },
        ).json()
        logger.debug(response)
        access_token = response.get("access_token")
        headers = {"Authorization": f"Bearer {access_token}"}
        users = requests.get("http://localhost:3001/api/users", headers=headers).json()
        logger.debug(users)
        return users
