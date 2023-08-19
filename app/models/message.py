import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.sql import functions
from geoalchemy2.types import Geography

from app.db.database import Base


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    

    text: Mapped[str]
    date_sent: Mapped[datetime.datetime] = Column(DateTime, nullable=False, server_default=functions.now())

    sender_id: Mapped[int] = mapped_column(ForeignKey("participants.id"))
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))

    sender = relationship("Participant", back_populates="messages")
    chat = relationship("Chat", back_populates="messages")
