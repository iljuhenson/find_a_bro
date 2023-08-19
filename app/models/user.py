from typing import List, Optional
import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from geoalchemy2.types import Geography

from app.db.database import Base
from app.models.participant import Participant


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str]
    
    first_name: Mapped[str]
    last_name: Mapped[str]
    
    description: Mapped[Optional[str]] = mapped_column(default="")

    #            There should be a path to default pfp   vvvvvvvvvv
    profile_picture_path: Mapped[Optional[str]] = mapped_column(default="")

    location = mapped_column(Geography(geometry_type="POINT"), nullable=True)
    location_update_date: Mapped[Optional[datetime.datetime]]
    
    is_active : Mapped[bool] = mapped_column(default=True)

    participant: Mapped[List["Participant"]] = relationship(back_populates="user")
