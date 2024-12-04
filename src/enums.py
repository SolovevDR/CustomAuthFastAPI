from enum import Enum, IntEnum


class TokensName(Enum):
    ACCESS_TOKEN = "access_token"
    REFRESH_TOKEN = "refresh_token"


class Role(IntEnum):
    USER = 1
    ADMIN = 2
