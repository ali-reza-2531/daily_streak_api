from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database_utils import Base
from datetime import date


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    total_xp = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    last_check_in_date = Column(Date, nullable=True)

    checkins = relationship("CheckIn", back_populates="user")


class CheckIn(Base):
    __tablename__ = "checkins"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    checkin_date = Column(Date, nullable=False, default=date.today)
    xp_earned = Column(Integer, default=10)

    user = relationship("User", back_populates="checkins")
