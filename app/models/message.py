from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import functions
from geoalchemy2.types import Geography

from app.db.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    sender_id = Column(ForeignKey("participants.id"))
    sender = relationship("Participant", back_populates="messages")

    text = Column(String, nullable=False)
    date_sent = Column(DateTime, nullable=False, server_default=functions.now())

    chat_id = Column(ForeignKey("chats.id"))
    chat = relationship("Chat", back_populates="messages")
