import traceback

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, PyJWKClientError

from config.setting import settings


class Auth0Oidc:
    def __init__(self):
        self.auth0_audience: str = settings.auth0_audience
        self.auth0_algorithm: str = settings.auth0_algorithm
        self.auth0_issuer: str = settings.auth0_issuer
        self.jwks_uri: str = f"{settings.auth0_issuer}.well-known/jwks.json"
        self.jwks_client = jwt.PyJWKClient(self.jwks_uri)

    def auth(self, login: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        try:
            token = login.credentials
            signing_key = self.jwks_client.get_signing_key_from_jwt(token).key

            payload = jwt.decode(
                token,
                signing_key,
                algorithms=self.auth0_algorithm,
                audience=self.auth0_audience,
                issuer=self.auth0_issuer,
                options={
                    "verify_signature": True,
                    "verify_aud": True,
                    "exp": True,
                },
            )
            return payload
        except PyJWKClientError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to verify credentials",
            )
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token has expired",
            )
        except InvalidTokenError:
            traceback.print_exc()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Bad credentials",
            )
