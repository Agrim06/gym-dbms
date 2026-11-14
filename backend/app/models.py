from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.sql import func
from .database import Base

class Trainer(Base):
    __tablename__ = "trainers"

    tid = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    salary = Column(Integer, nullable=False)
    email = Column(String, nullable=False)


class Member(Base):
    __tablename__ = "members"

    uid = Column(Integer, primary_key=True)
    tid = Column(Integer, ForeignKey("trainers.tid"), nullable=True)
    name = Column(String, nullable=False)
    fees = Column(Integer, nullable=False)
    joining_date = Column(DateTime, nullable=False)


class Membership(Base):
    __tablename__ = "memberships"

    membership_id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("members.uid"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)


class Payment(Base):
    __tablename__ = "payments"

    pid = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("members.uid"), nullable=False)
    amount = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)


class Attendance(Base):
    __tablename__ = "attendance_log"

    attendance_id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("members.uid"), nullable=False)
    date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)


class WorkoutSchedule(Base):
    __tablename__ = "schedules"

    schedule_id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("members.uid"), nullable=False)
    trainer_id = Column(Integer, ForeignKey("trainers.tid"), nullable=False)
    workout_details = Column(String, nullable=False)
