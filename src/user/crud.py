from typing import Union

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import User, Role
from user.scheme import UserInfo, UsersInfo


async def select_user_for_register(
    session: AsyncSession, login: str, email: str
) -> Union[int, None]:
    query = (
        select(User.id).where(or_(User.login == login, User.email == email))
    )
    result = await session.execute(query)
    return result.scalar()


async def add_new_user(
    session: AsyncSession, login: str, password: str, email: str
) -> int:
    user = User(
        login=login,
        password=password,
        email=email
    )
    session.add(user)
    await session.flush()
    await session.commit()


async def select_user_info(session: AsyncSession, user_id: int) -> UserInfo:
    query = (
        select(
            User.email,
            User.login,
            User.last_loging,
            Role.name.label("role_name")
        )
        .filter(User.id == user_id)
        .join(User.role_id)
    )
    result = await session.execute(query)
    result = result.first()
    return UserInfo.from_orm(result)


async def select_users_info(session: AsyncSession) -> UsersInfo:
    query = (
        select(
            User.email,
            User.login,
            User.last_loging,
            Role.name.label("role_name")
        )
        .join(User.role_id)
    )
    result = await session.execute(query)
    result = result.all()
    result = [UserInfo.from_orm(user) for user in result]
    return result
