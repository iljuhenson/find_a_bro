from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from geoalchemy2.types import Geography

from app.db.database import Base


class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    user_id = Column(ForeignKey("users.id"))
    user = relationship("User", back_populates="participant")
    route = Column(Geography(geometry_type="LINESTRING"), nullable=True)
    
    meeting_id = Column(ForeignKey("meetings.id"))
    meeting = relationship("Meeting", back_populates="participants")

    messages = relationship("Message", back_populates="sender")
