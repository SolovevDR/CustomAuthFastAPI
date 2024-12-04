from pydantic import BaseModel


class UserLogin(BaseModel):
    login_email: str
    password: str


class Tokens(BaseModel):
    access_token: str
    refresh_token: str


class AccessTokens(BaseModel):
    access_token: str


class Auth(BaseModel):
    login_email: str
    password: str
