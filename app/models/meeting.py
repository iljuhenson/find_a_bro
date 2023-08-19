import datetime
from typing import Optional, List

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from geoalchemy2.types import Geography

from app.db.database import Base
from app.models.chat import Chat


class Meeting(Base):
    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    
    meeting_place = mapped_column(Geography(geometry_type="POINT"), nullable=True)
    meeting_initialization_date: Mapped[Optional[datetime.datetime]]
    

    chat: Mapped[Optional["Chat"]] = relationship(back_populates="meeting")
    participants: Mapped[List["Participant"]] = relationship(back_populates="meeting")
