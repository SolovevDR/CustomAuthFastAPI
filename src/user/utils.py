from fastapi import Response

from enums import TokensName


async def delete_token(response: Response) -> None:
    for token_name in TokensName:
        response.set_cookie(
            key=token_name.value,
            value="",
            httponly=True,
            max_age=0
        )
