from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    description = Column(String, nullable=True, default="")

    #            There should be a path to default pfp   vvvvvvvvvv
    profile_picture_path = Column(String, nullable=True, default="") 
    
    is_active = Column(Boolean, default=True)
