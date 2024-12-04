from fastapi import Depends, Response, APIRouter, Request
from sqlalchemy.ext.asyncio import AsyncSession

from auth.crud import select_user, update_user_last_login
from database import get_async_session
from auth.utils import generate_tokens, delete_cookie, set_cookie
from auth.scheme import Tokens, AccessTokens, Auth
from depends.token import TokenInfo, check_user_token
from exceptions.exceptions import LoginError
from passwordutils import check_password
from user.scheme import StatusSuccess

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=AccessTokens)
async def login(
    response: Response,
    auth_value: Auth,
    session: AsyncSession = Depends(get_async_session),
):
    result = await select_user(session=session, login_email=auth_value.login_email)
    if result.disabled:
        raise LoginError
    await check_password(
        value_password=auth_value.password, user_password=result.password
    )
    access_token, refresh_token = await generate_tokens(user_id=result.id)
    await set_cookie(refresh_token=refresh_token, response=response)
    await update_user_last_login(session=session, user_id=result.id)
    return AccessTokens(access_token=access_token)


@router.get("/logout", response_model=StatusSuccess)
async def logout(response: Response):
    await delete_cookie(response=response)
    return StatusSuccess()


@router.post("/refresh", response_model=Tokens)
async def refresh(
    response: Response,
    request: Request,
    authorization_info: TokenInfo = Depends(check_user_token),
):
    return Tokens(
        access_token=authorization_info.access_token,
        refresh_token=authorization_info.refresh_token
    )
