from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .services import member_services, trainer_services
from .database import get_db
from .schemas import Member, Trainer, TrainerCreate, Membership, Payment, MemberCreate, MemberUpdate
from . import models
from typing import List

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