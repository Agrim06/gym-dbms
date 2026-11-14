from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Index, ForeignKey
from sqlalchemy.sql import func
from .database import Base

class Trainer(Base):

    __tablename__ = "trainers"
    tid = Column(Integer, primary_key= True)
    name = Column(String, nullable=False)
    salary = Column(Integer, nullable=False)
    email = Column(String, nullable=False)

class Member(Base):

    __tablename__ = "members"
    uid = Column(Integer, primary_key= True)
    tid = Column(Integer, ForeignKey("trainers.tid"), nullable= True)
    name = Column(String, nullable=False)
    fees = Column(Integer, nullable=False)
    joining_date = Column(DateTime , nullable= False)