from sqlalchemy import Column, Integer, String, DateTime, BOOLEAN, ForeignKey
from datetime import datetime

from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    login = Column(String)
    password = Column(String)
    email = Column(String)
    role = Column(Integer, ForeignKey("role.id"), default=1)
    disabled = Column(BOOLEAN, default=False)
    last_loging = Column(DateTime, default=datetime.utcnow())

    role_id = relationship("Role", back_populates="owner")


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)

    owner = relationship("User", back_populates="role_id")
