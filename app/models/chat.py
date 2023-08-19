import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.sql import functions

from app.db.database import Base


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)

    text: Mapped[str]
    date_sent: Mapped[Optional[datetime.datetime]] = mapped_column(nullable=False, server_default=functions.now())

    meeting_id: Mapped[Optional[int]] = mapped_column(ForeignKey("meetings.id"))

    meeting: Mapped[Optional["Meeting"]] = relationship(back_populates="chat")
