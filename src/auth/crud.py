from datetime import datetime

from sqlalchemy import select, update, or_
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import User


async def select_user(session: AsyncSession, login_email: str) -> User:
    query = select(User).where(or_(User.login == login_email, User.email == login_email))
    result = await session.execute(query)
    result = result.scalar()
    return result


async def update_user_last_login(session: AsyncSession, user_id: int) -> None:
    query = (
        update(User).values({"last_loging": datetime.now()}).filter(User.id == user_id)
    )
    await session.execute(query)
    await session.commit()
