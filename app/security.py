from fastapi import Depends, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from jose.jwt import encode, decode
from sqlalchemy.orm import Session
import schemas
from db.models import User
from db.database import get_db
import settings

api_key_header = APIKeyHeader(name="api-key", auto_error=False)


def get_apikey_header(api_key: str = Depends(api_key_header)) -> str:
    """
    Функция возвращает api-key.

    :param api_key: любое слово или сочетание слов.
    :return: зашифрованная строка.
    """
    # encoded_jwt = encode(
    #     claims={"api-key": api_key},
    #     key=settings.SECRET_KEY,
    #     algorithm=settings.ALGORITHM,
    # )
    # if api_key is None:
    #     encoded_jwt = encode(
    #         claims={"api-key": None},
    #         key=settings.SECRET_KEY,
    #         algorithm=settings.ALGORITHM,
    #     )
    # payload = decode(encoded_jwt, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    # return encoded_jwt
    return api_key


def decode_key(encoded_api_key: str):
    payload = decode(
        encoded_api_key, settings.SECRET_KEY, algorithms=settings.ALGORITHM
    )
    api_key: str = payload.get("api-key")
    return api_key


def get_current_user(
    api_key=Depends(get_apikey_header), db: Session = Depends(get_db)
) -> schemas.UserFull:
    current_user = db.query(User).filter(User.api_key == api_key).first()
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user or key"
        )
    return current_user
