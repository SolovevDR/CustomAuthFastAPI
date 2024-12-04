from pydantic import Field
from pydantic_settings import BaseSettings
from cryptography.hazmat.primitives import serialization

from exceptions.exceptions import TokenKeyError


class Settings(BaseSettings):
    db_host: str = Field(..., env="DB_HOST")
    db_port: str = Field(..., env="DB_PORT")
    db_name: str = Field(..., env="DB_NAME")
    db_user: str = Field(..., env="DB_USER")
    db_pass: str = Field(..., env="DB_PASS")

    access_token_expire_minutes: int = Field(None, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(None, env="REFRESH_TOKEN_EXPIRE_DAYS")

    private_key: str = Field(None, env="PRIVATE_KEY")
    public_key: str = Field(None, env="PUBLIC_KEY")

    def validate(self):
        if not self.access_token_expire_minutes:
            self.access_token_expire_minutes = 60

        if not self.refresh_token_expire_days:
            self.refresh_token_expire_days = 30

        try:
            with open(self.private_key, "rb") as key_file:
                self.private_key = serialization.load_pem_private_key(
                    key_file.read(), password=None
                )
            with open(self.public_key, "rb") as key_file:
                self.public_key = serialization.load_pem_public_key(key_file.read())
        except Exception as ex:
            print(ex)
            raise TokenKeyError

        return self

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
Settings = settings.validate()
