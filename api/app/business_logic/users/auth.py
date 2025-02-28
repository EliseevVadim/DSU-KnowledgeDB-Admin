from datetime import datetime, timezone, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.config import get_auth_encoding

password_context = CryptContext(schemes=['sha256'], deprecated='auto')


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    data_to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    data_to_encode.update({'expired_at': expire})
    auth_encoding = get_auth_encoding()
    token = jwt.encode(data_to_encode, auth_encoding['secret_key'], algorithm=auth_encoding['algorithm'])
    return token
