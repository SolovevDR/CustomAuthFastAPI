from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from config import Settings

DATABASE_URL = (
    f"postgresql+asyncpg://{Settings.db_user}:{Settings.db_pass}@"
    f"{Settings.db_host}:{Settings.db_port}/{Settings.db_name}"
)
Base = declarative_base()
metadata = MetaData()
