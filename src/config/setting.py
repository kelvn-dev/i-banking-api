from functools import lru_cache

from pydantic import AnyHttpUrl, EmailStr, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    auth0_domain: str
    auth0_issuer: str
    auth0_audience: str
    auth0_algorithm: str

    auth0_client_id: str
    auth0_client_secret: str
    auth0_client_audience: str

    db_uri: str
    db_schema: str

    otp_secret: str

    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=False, extra="ignore"
    )


# Reading the env file is costly, especially when read for each request. So cache the values using lru_cache.
@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
