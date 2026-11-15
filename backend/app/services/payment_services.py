from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models
from ..schemas import Payment, PaymentCreate
from datetime import datetime, date
from typing import Optional

def create_payment(db :Session, payment_data : PaymentCreate):
    payment = models.Payment(
        member_id = payment_data.member_id,
        amount = payment_data.amount,
        date = payment_data.date,
        status = payment_data.status
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def get_payment(db:Session, member_id : int) -> List[models.Payment]:
    return db.query(models.Payment).filter(models.Payment.member_id == member_id).all()

def get_revenue(db: Session) -> int:
    return db.query(func.sum(models.Payment.amount)).filter(models.Payment.status == "Completed").scalar() or 0