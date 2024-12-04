from fastapi import Depends, Response, APIRouter
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from depends.token import TokenInfo, check_user_token, check_admin_token
from exceptions.exceptions import RoleError
from passwordutils import create_password
from user.crud import (
    select_user_info,
    select_user_for_register,
    add_new_user,
    select_users_info
)
from user.scheme import StatusSuccess, UserInfo, UserCreate, UsersInfo

router = APIRouter(prefix="/api/v1/user", tags=["user"])


@router.post("/register", response_model=StatusSuccess)
async def register(
    response: Response,
    user_value: UserCreate,
    session: AsyncSession = Depends(get_async_session),
):
    result = await select_user_for_register(
        session=session, login=user_value.login, email=user_value.email
    )
    if result:
        raise RoleError

    password = await create_password(user_value.password)
    await add_new_user(
        session=session,
        login=user_value.login,
        password=password,
        email=user_value.email
    )
    return StatusSuccess()


@router.get("/all", response_model=UsersInfo)
async def select_user(
    response: Response,
    request: Request,
    authorization_info: TokenInfo = Depends(check_admin_token),
    session: AsyncSession = Depends(get_async_session)
):
    result = await select_users_info(session=session)
    return UsersInfo(users=result)


@router.get("/{user_id}", response_model=UserInfo)
async def select_user(
    response: Response,
    request: Request,
    user_id: int,
    authorization_info: TokenInfo = Depends(check_user_token),
    session: AsyncSession = Depends(get_async_session)
):
    result = await select_user_info(session=session, user_id=user_id)
    return result
