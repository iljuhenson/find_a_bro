from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from geoalchemy2.types import Geometry

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    description = Column(String, nullable=True, default="")

    #            There should be a path to default pfp   vvvvvvvvvv
    profile_picture_path = Column(String, nullable=True, default="")

    location = Column(Geometry(geometry_type="POINT"), nullable=True)
    location_update_date = Column(DateTime, nullable=True)
    
    is_active = Column(Boolean, default=True)

    participant = relationship("Participant", back_populates="user")
