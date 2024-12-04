from fastapi import FastAPI
from starlette.responses import JSONResponse

from exceptions.exceptions import (
    LoginError,
    RoleError,
    NotFoundError,
    TokenError,
)


def add_exception_handler(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def validation_exception_handler(request, err):
        return JSONResponse(
            status_code=401,
            content={
                "status": "error",
                "error_details": "bad request",
            },
        )

    @app.exception_handler(LoginError)
    async def validation_exception_handler(request, err):
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "error_details": str(err),
            },
        )

    @app.exception_handler(RoleError)
    async def validation_exception_handler(request, err):
        return JSONResponse(
            status_code=403,
            content={
                "status": "error",
                "error_details": str(err),
            },
        )

    @app.exception_handler(TokenError)
    async def validation_exception_handler(request, err):
        return JSONResponse(
            status_code=403,
            content={
                "status": "error",
                "error_details": str(err),
            },
        )

    @app.exception_handler(NotFoundError)
    async def validation_exception_handler(request, err):
        return JSONResponse(
            status_code=404,
            content={
                "status": "error",
                "error_details": str(err),
            },
        )
