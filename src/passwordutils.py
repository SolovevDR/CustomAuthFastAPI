from typing import Optional, Union

from passlib.hash import bcrypt

from exceptions.exceptions import LoginError


async def create_password(password: str = None) -> Union[str, None]:
    if password:
        return bcrypt.hash(password)


async def check_password(value_password: str, user_password: str) -> None:
    if not bcrypt.verify(value_password, user_password):
        raise LoginError
