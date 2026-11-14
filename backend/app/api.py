from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .services import member_services
from .database import get_db
from .schemas import Member, Trainer, Membership, Payment, MemberCreate, MemberUpdate
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

@router.post("/create", response_model= MemberCreate)
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