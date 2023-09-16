from typing import List

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from geoalchemy2.types import Geography

from app.db.database import Base
from app.models.meeting import Meeting 



class Participant(Base):
    __tablename__ = "participants"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    
    route = mapped_column(Geography(geometry_type="LINESTRING"), nullable=True)
    has_agreed: Mapped[bool] = mapped_column(default=False)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id"))

    user: Mapped["User"] = relationship(back_populates="participant")
    meeting: Mapped["Meeting"] = relationship(back_populates="participants")
    messages: Mapped[List["Message"]] = relationship(back_populates="sender")
