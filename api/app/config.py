import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str
    REGISTRATION_SECRET: str
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"),
        extra='allow'
    )


settings = Settings()


def get_connection_string():
    return (f"postgresql+psycopg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}"
            f":{settings.DB_PORT}/{settings.DB_NAME}")


def get_auth_encoding():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}


def get_registration_secret():
    return settings.REGISTRATION_SECRET
