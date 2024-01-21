from functools import lru_cache

from pydantic import AnyHttpUrl, BaseSettings, EmailStr


class Settings(BaseSettings):
    auth0_domain: str
    auth0_issuer: AnyHttpUrl
    auth0_audience: str
    auth0_algorithm: str

    class Config:
        env_file = ".env"
        case_sensitive = False


# Reading the env file is costly, especially when read for each request. So cache the values using lru_cache.
@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
