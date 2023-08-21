import datetime
from typing import Optional, List

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.sql import functions

from app.db.database import Base
from app.models.message import Message

class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)

    meeting_id: Mapped[Optional[int]] = mapped_column(ForeignKey("meetings.id"))

    messages: Mapped[List["Message"]] = relationship(back_populates="chat")
    meeting: Mapped[Optional["Meeting"]] = relationship(back_populates="chat")
