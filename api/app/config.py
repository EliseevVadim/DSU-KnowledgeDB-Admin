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
    UPLOAD_DIR: str
    MODEL_NAME: str
    MODEL_REVISION: str
    COLLECTION_NAME: str
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


def get_upload_dir():
    return settings.UPLOAD_DIR


def get_model_name():
    return settings.MODEL_NAME


def get_model_revision():
    return settings.MODEL_REVISION


def get_collection_name():
    return settings.COLLECTION_NAME
