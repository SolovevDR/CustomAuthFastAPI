from dataclasses import dataclass
from typing import Optional

from fastapi import Security, Depends, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import is_token_valid, refresh_tokens, set_cookie, set_headers
from depends.crud import select_user_info
from exceptions.exceptions import RoleError, TokenError
from database import get_async_session
from enums import Role, TokensName


@dataclass
class TokenInfo:
    user_id: Optional[int] = 0
    login: Optional[str] = None
    email: Optional[str] = None
    role: Optional[int] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None


optional_security = HTTPBearer(auto_error=False)
security = HTTPBearer()


async def create_tokens(
    access_token: str,
    refresh_token: str,
    response: Response,
    session: AsyncSession
) -> TokenInfo:
    if (
            not await is_token_valid(token=access_token)
            and not await is_token_valid(token=refresh_token)
    ):
        raise TokenError
    access_token, refresh_token, user_id = await refresh_tokens(
        refresh_token=refresh_token
    )
    await set_cookie(response=response, refresh_token=refresh_token)
    await set_headers(response=response, access_token=access_token)
    result = await select_user_info(session=session, user_id=user_id)
    return TokenInfo(
        user_id=user_id,
        login=result.login,
        email=result.email,
        role=result.role,
        access_token=access_token,
        refresh_token=refresh_token
    )


async def check_user_token(
    user_id: int,
    response: Response,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Security(security),
    session: AsyncSession = Depends(get_async_session),
) -> TokenInfo:
    access_token = credentials.credentials
    refresh_token = request.cookies.get(TokensName.REFRESH_TOKEN.value)
    user_info = await create_tokens(
        access_token=access_token,
        refresh_token=refresh_token,
        response=response,
        session=session
    )
    if user_info.user_id != user_id and user_info.role != Role.ADMIN.value:
        raise RoleError
    return user_info


async def check_admin_token(
    response: Response,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Security(security),
    session: AsyncSession = Depends(get_async_session),
) -> TokenInfo:
    access_token = credentials.credentials
    refresh_token = request.cookies.get(TokensName.REFRESH_TOKEN.value)
    user_info = await create_tokens(
        access_token=access_token,
        refresh_token=refresh_token,
        response=response,
        session=session
    )
    if user_info.role != Role.ADMIN.value:
        raise RoleError
    return user_info
