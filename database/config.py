from pydantic import Field
from pydantic_settings import BaseSettings
from passlib.hash import bcrypt


class Settings(BaseSettings):
    db_host: str = Field(..., env="DB_HOST")
    db_port: str = Field(..., env="DB_PORT")
    db_name: str = Field(..., env="DB_NAME")
    db_user: str = Field(..., env="DB_USER")
    db_pass: str = Field(..., env="DB_PASS")

    login: str = Field(..., env="ADMIN_LOGIN")
    password: str = Field(..., env="ADMIN_PASSWORD")
    email: str = Field(..., env="ADMIN_EMAIL")
    role: int = Field(..., env="ROLE")

    def validate(self):
        self.password = bcrypt.hash(self.admin_password)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


Settings = Settings()
