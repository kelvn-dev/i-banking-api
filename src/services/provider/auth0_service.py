from auth0.management import Auth0
from fastapi import Depends

from config.auth0_client import auth0_client


class Auth0Service:

    auth0_database_api = auth0_client.get_database_api()
    auth0_management_api = auth0_client.get_management_api()

    def get_by_id(self, id: str):
        return self.auth0_management_api.users.get(id)


auth0_service = Auth0Service()
