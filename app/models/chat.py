from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import functions
from geoalchemy2.types import Geography

from app.db.database import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    text = Column(String, nullable=False)
    date_sent = Column(DateTime, nullable=False, server_default=functions.now())

    meeting_id = Column(ForeignKey("meetings.id"))
    meeting = relationship("Meeting", back_populates="chat")
