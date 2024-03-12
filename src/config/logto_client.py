import time

from auth0.authentication import Database, GetToken
from auth0.management import Auth0
from loguru import logger

from config.setting import settings


class Auth0Client:
    def __init__(self):
        self.token_api: GetToken = None
        self.database_api: Database = None
        self.management_token: str = None
        self.management_token_expiry: int = None
        self.management_api: Auth0 = None

    def get_token_api(self):
        if not self.token_api:
            self.token_api = GetToken(
                domain=settings.auth0_domain,
                client_id=settings.auth0_client_id,
                client_secret=settings.auth0_client_secret,
            )
        return self.token_api

    def get_database_api(self):
        if not self.database_api:
            self.database_api = Database(
                domain=settings.auth0_domain,
                client_id=settings.auth0_client_id,
                client_secret=settings.auth0_client_secret,
            )
        return self.database_api

    def renew_management_token(self):
        self.management_token = self.get_token_api().client_credentials(
            settings.auth0_client_audience
        )
        self.management_token_expiry = (
            int(time.time()) + self.management_token["expires_in"]
        )

    def get_management_api(self):
        if self.management_token and self.management_token_expiry > int(time.time()):
            logger.debug("Token has not expired, using existing token")
        else:
            logger.debug("Existing access token has expired")
            self.renew_management_token()
        self.management_api = Auth0(
            settings.auth0_domain, self.management_token["access_token"]
        )
        return self.management_api


auth0_client = Auth0Client()
