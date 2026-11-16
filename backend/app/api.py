from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .services import member_services, trainer_services, membership_services, payment_services, attendance_services
from .database import get_db
from .schemas import Member, Trainer, TrainerCreate, Membership,MembershipCreate, MembershipRenew, Payment, PaymentCreate,  MemberCreate, MemberUpdate,Attendance, AttendanceHistory,  WorkoutSchedule, WorkoutScheduleCreate
from . import models
from typing import List
from datetime import date, datetime

router = APIRouter(prefix="/gym")

@router.get("/all", response_model= List[Member])
def get_all_members(db : Session = Depends(get_db)):
    return member_services.get_all_members(db)

@router.get("/member/{uid}", response_model= Member)
def get_member_info(uid : int , db: Session = Depends(get_db)):
    data = member_services.get_member_by_id(db, uid)

    if not data:
        raise HTTPException(status_code=404, detail=f"Member with '{uid}' not found")

    return data

@router.post("/create", response_model= Member)
def create_member(payload : MemberCreate , db: Session = Depends(get_db)):
    data = member_services.create_member(db, payload)

    return data

@router.put("/member/{uid}", response_model=Member)
def update_member(uid: int, payload: MemberUpdate, db: Session = Depends(get_db)):
    updated_member = member_services.update_member(db, uid, payload)
    if not updated_member:
        raise HTTPException(status_code=404, detail=f"Member with id '{uid}' not found")
    return updated_member

@router.delete("/member/{uid}")
def delete_member(uid: int, db: Session = Depends(get_db)):
    success = member_services.delete_member(db, uid)
    if not success:
        raise HTTPException(status_code=404, detail=f"Member with id '{uid}' not found")
    return {"message": f"Member with id '{uid}' deleted successfully"}


@router.get("/trainers", response_model=List[Trainer])
def get_all_trainers(db: Session = Depends(get_db)):
    return trainer_services.get_all_trainers(db)

@router.get("/trainers/{tid}", response_model=Trainer)
def get_trainer_info(tid: int, db: Session = Depends(get_db)):
    trainer = trainer_services.get_trainer_by_id(db, tid)
    if not trainer:
        raise HTTPException(status_code=404, detail=f"Trainer with id '{tid}' not found")
    return trainer

@router.post("/trainers", response_model=Trainer, status_code=201)
def create_trainer(payload: TrainerCreate, db: Session = Depends(get_db)):
    return trainer_services.create_trainer(db, payload)

@router.get("/trainers/{tid}/members", response_model=List[Member])
def get_trainer_members(tid: int, db: Session = Depends(get_db)):
    trainer = trainer_services.get_trainer_by_id(db, tid)
    if not trainer:
        raise HTTPException(status_code=404, detail=f"Trainer with id '{tid}' not found")
    return trainer_services.get_trainer_members(db, tid)


@router.post("/memberships", response_model= Membership)
def create_membership(payload : MembershipCreate , db : Session = Depends(get_db)):
    membership = membership_services.new_membership(
        db=db,
        member_id=payload.member_id,
        start_date=payload.start_date,
        end_date=payload.end_date,
        status=payload.status
    )
    if not membership:
        raise HTTPException(status_code=404, detail=f"Member with id '{payload.member_id}' not found")
    return membership

@router.put("/memberships/{membership_id}/renew", response_model=Membership)
def renew_membership(payload: MembershipRenew, membership_id: int, db: Session = Depends(get_db)):
    membership = membership_services.renew_membership(
        db=db,
        membership_id=membership_id,
        end_date=payload.new_end_date,
        status=payload.status
    )
    if not membership:
        raise HTTPException(status_code=404, detail=f"Failed to renew: membership '{membership_id}' not found")
    return membership

@router.get("/memberships/expiring", response_model=List[Membership])
def expiring_memberships(db: Session = Depends(get_db)):
    return membership_services.expiring_memberships(db, days=7)


@router.post("/payments/create", response_model=Payment, status_code=201)
def create_payment(payload: PaymentCreate, db: Session = Depends(get_db)):
    payment = payment_services.create_payment(db, payload)
    return payment

@router.get("/payments/member/{uid}", response_model=List[Payment])
def get_payment(uid: int, db: Session = Depends(get_db)):
    history = payment_services.get_payment(db, uid)

    if not history:
        raise HTTPException(status_code=404, detail=f"Payment for member with id '{uid}' not found")
    return history

@router.get("/payments/revenue")
def get_revenue(db: Session = Depends(get_db)):
    revenue = payment_services.get_revenue(db)
    return {"total_revenue": revenue}

@router.post("/attendance/check-in", response_model=Attendance, status_code=201)
def checkin(member_id: int, date: date, status: str = "Present", db: Session = Depends(get_db)):
    data = attendance_services.checkin(db, member_id, date, status)

    if not data:
        raise HTTPException(status_code=404, detail=f"Member with id '{member_id}' not found")
    return data

@router.get("/attendance/member/{uid}", response_model=List[AttendanceHistory])
def get_attendance(uid: int, db: Session = Depends(get_db)):
    attendance = attendance_services.get_attendance(db, uid)    

    if not attendance:
        raise HTTPException(status_code=404, detail=f"Attendance for member with id '{uid}' not found")
    return attendance

@router.post("/schedules", response_model=WorkoutSchedule, status_code=201)
def create_schedule(payload: WorkoutScheduleCreate, db: Session = Depends(get_db)):
    schedule = attendance_services.create_schedule(db, payload)
    if not schedule:
        raise HTTPException(status_code=404, detail=f"Member with id '{payload.member_id}' not found")
    return schedule

@router.get("/schedules/member/{uid}", response_model= List[WorkoutSchedule])
def get_schedule(uid : int , db : Session = Depends(get_db)):
    schedule = attendance_services.get_schedule(db, uid)

    if not schedule:
        raise HTTPException(status_code=404, detail=f"Schedules with id '{uid}' not found")
    
    return schedule