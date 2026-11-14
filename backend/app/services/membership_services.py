from sqlalchemy.orm import Session
from .. import models
from ..schemas import Membership, MembershipCreate, MembershipRenew
from datetime import date, datetime, timedelta

def new_membership(db : Session, member_id : int, start_date: date, end_date : date, status : str = "Active"):
    db_member = db.query(models.Member).filter(models.Member.uid == member_id).first()
    if not db_member:
        return None
    
    db_membership = models.Membership(
        member_id=member_id,
        start_date=start_date,
        end_date=end_date,
        status=status
    )

    db.add(db_membership)
    db.commit()
    db.refresh(db_membership)
    return db_membership

def renew_membership(db : Session, membership_id : int, end_date : date, status : str = "Active"):
    membership = db.query(models.Membership).filter(models.Membership.membership_id == membership_id).first()
    if not membership:
        return None

    membership.end_date = end_date
    membership.status = status
    db.commit()
    db.refresh(membership)
    return membership
    
def expiring_memberships(db: Session, days: int = 7) -> list[models.Membership]:
    threshold_date = date.today() + timedelta(days=days)
    return db.query(models.Membership).filter(
        models.Membership.status == "Active",
        models.Membership.end_date <= threshold_date,
        models.Membership.end_date >= date.today()
    ).all()

