from fastapi import Depends
from fastapi.security.api_key import APIKeyHeader
from jose.jwt import encode, decode
import settings

api_key_header = APIKeyHeader(name="api-key", auto_error=False)


def get_apikey_header(api_key: str = Depends(api_key_header)) -> str:
    """
    Функция возвращает api-key.

    :param api_key: любое слово или сочетание слов.
    :return: зашифрованная строка.
    """
    # print(api_key, 1111111111111)
    encoded_jwt = encode(
        claims={"api-key": api_key},
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    if api_key is None:
        encoded_jwt = encode(
            claims={"api-key": None},
            key=settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
    payload = decode(encoded_jwt, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    # api_key: str = payload.get("api-key")
    # print(api_key, 13123123123213213123123123123)
    return encoded_jwt


def decode_key(encoded_api_key: str):
    payload = decode(encoded_api_key, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    api_key: str = payload.get("api-key")
    return api_key
