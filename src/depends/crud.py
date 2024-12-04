from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import User
from exceptions.exceptions import NotFoundError


async def select_user_info(session: AsyncSession, user_id: str) -> User:
    query = select(User.login, User.email, User.role).filter(User.id == user_id)
    result = await session.execute(query)
    result = result.one()
    if result:
        return result
    else:
        raise NotFoundError
