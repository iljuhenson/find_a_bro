from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from geoalchemy2.types import Geography

from app.db.database import Base


class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    meeting_place = Column(Geography(geometry_type="POINT"), nullable=True)
    meeting_initialization_date = Column(DateTime, nullable=True)
    
    participants = relationship("Participant", back_populates="participants")

    chat = relationship("Chat", uselist=False, back_populates="meeting")
