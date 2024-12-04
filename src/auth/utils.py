from datetime import datetime, timedelta
from typing import Tuple

import jwt
from fastapi import Response
from fastapi.security import HTTPBearer


from config import Settings
from exceptions.exceptions import TokenError
from enums import TokensName


security = HTTPBearer()


async def set_cookie(refresh_token: str, response: Response) -> Response:
    response.set_cookie(
        key=TokensName.REFRESH_TOKEN.value,
        value=refresh_token,
        httponly=True,
        max_age=Settings.access_token_expire_minutes * 24 * 60 * 60,
    )
    return response


async def delete_cookie(response: Response) -> Response:
    response.set_cookie(
        key=TokensName.REFRESH_TOKEN.value,
        value="",
        httponly=True,
        max_age=0,
    )
    return response


async def set_headers(access_token: str, response: Response) -> Response:
    response.headers["Authorization"] = f"Bearer: {access_token}"
    return response


async def generate_token_payload(type_token: str, user_id: int) -> dict:
    exp = None
    if type_token == TokensName.ACCESS_TOKEN.value:
        exp = datetime.utcnow() + timedelta(minutes=Settings.access_token_expire_minutes)
    elif type_token == TokensName.REFRESH_TOKEN.value:
        exp = datetime.utcnow() + timedelta(minutes=Settings.refresh_token_expire_days)
    return {
        "id": user_id,
        "exp": exp,
        "type": type_token
    }


async def generate_token(type_token: str, user_id: int) -> str:
    return jwt.encode(
        await generate_token_payload(type_token=type_token, user_id=user_id),
        Settings.private_key,
        algorithm="RS256"
    )


async def generate_tokens(user_id: int):
    access_token = await generate_token(
        type_token=TokensName.ACCESS_TOKEN.value,
        user_id=user_id
    )
    refresh_token = await generate_token(
        type_token=TokensName.REFRESH_TOKEN.value,
        user_id=user_id
    )

    return access_token, refresh_token


async def is_token_valid(token: str) -> bool:
    try:
        payload = jwt.decode(token, Settings.public_key, algorithms=["RS256"])
    except jwt.ExpiredSignatureError:
        return False
    except (jwt.InvalidTokenError, KeyError):
        return False

    if (
            payload["type"] != TokensName.ACCESS_TOKEN.value
            and payload["type"] != TokensName.REFRESH_TOKEN.value
    ):
        return False

    return datetime.utcnow() < datetime.fromtimestamp(payload["exp"])


async def refresh_tokens(refresh_token) -> Tuple[str, str, int]:
    try:
        payload = jwt.decode(refresh_token, Settings.public_key, algorithms=["RS256"])
        access_token, refresh_token = await generate_tokens(payload["id"])
        return access_token, refresh_token, payload["id"]
    except (jwt.InvalidTokenError, KeyError):
        raise TokenError
