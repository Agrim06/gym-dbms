from typing import List, Optional

from sqlalchemy.orm import Session
from .. import models

from ..schemas import Trainer, TrainerCreate


def get_all_trainers(db: Session, skip: int = 0, limit: int = 100) -> list[models.Trainer]:

    return db.query(models.Trainer).offset(skip).limit(limit).all()


def create_trainer(db: Session, data: TrainerCreate):
    db_trainer = models.Trainer(
        name=data.name,
        salary=data.salary,
        email=data.email
    )
    db.add(db_trainer)
    db.commit()
    db.refresh(db_trainer)
    return db_trainer

def get_trainer_by_id(db: Session, trainer_id: int) -> Optional[models.Trainer]:
    return db.query(models.Trainer).filter(models.Trainer.tid == trainer_id).first()


def get_trainer_members(db: Session, trainer_id: int) -> list[models.Member]:
    return db.query(models.Member).filter(models.Member.tid == trainer_id).all()