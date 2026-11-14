from typing import List, Optional
from sqlalchemy.orm import Session
from .. import models
from ..schemas import Member , MemberCreate

def create_member(db: Session, member_data: MemberCreate):
    db_member = models.Member(
        name=member_data.name,
        fees=member_data.fees,
        tid=member_data.tid,
        joining_date=member_data.joining_date
    )

    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def get_all_members(db: Session, skip: int = 0, limit: int = 100) -> list[models.Member]:
    return db.query(models.Member).offset(skip).limit(limit).all()

def get_member_by_id(db: Session, member_id: int) -> Optional[models.Member]:
    return db.query(models.Member).filter(models.Member.uid == member_id).first()

def update_member(db: Session, member_id : int , update_data : schemas.MemberUpdate):
    db_member = db.query(models.Member).filter(models.Member.uid == member_id).first()
    if not db_member:
        return None
    
    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(db_member, key, value)
    db.commit()
    db.refresh(db_member)
    return db_member

def delete_member(db: Session, member_id: int) -> bool:
    db_member = db.query(models.Member).filter(models.Member.uid == member_id).first()
    if not db_member:
        return False
    db.delete(db_member)
    db.commit()
    return True