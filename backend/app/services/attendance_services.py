from sqlalchemy.orm import Session
from .. import models
from ..schemas import Attendance, AttendanceHistory, WorkoutSchedule, WorkoutScheduleCreate
from datetime import datetime, date


def checkin(db : Session, member_id : int, date : date, status : str = "Present"):
    db_member = db.query(models.Member).filter(models.Member.uid == member_id).first()
    if not db_member:
        return None

    data = models.Attendance(
        member_id = member_id,
        date = date,
        status = status
    )

    db.add(data)
    db.commit()
    db.refresh(data)
    return data

def get_attendance(db : Session, member_id : int) -> list[models.Attendance]:
    return db.query(models.Attendance).filter(models.Attendance.member_id == member_id).all()

def create_schedule(db : Session, payload : WorkoutScheduleCreate):
    db_member = db.query(models.Member).filter(models.Member.uid == payload.member_id).first()
    if not db_member:
        return None

    data = models.WorkoutSchedule(
        member_id = payload.member_id,
        trainer_id = payload.trainer_id,
        workout_details = payload.workout_details
    )

    db.add(data)
    db.commit()
    db.refresh(data)
    return data

def get_schedule(db: Session, member_id: int) -> list[models.WorkoutSchedule] | None:
    db_member = db.query(models.Member).filter(models.Member.uid == member_id).first()
    if not db_member:
        return None
    
    return db.query(models.WorkoutSchedule).filter(models.WorkoutSchedule.member_id == member_id).all()
