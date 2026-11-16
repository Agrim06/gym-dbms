from pydantic import BaseModel
from datetime import date

class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

class Member(BaseSchema):
    uid: int
    name: str
    fees: int
    tid: int | None = None
    joining_date: date

class MemberCreate(BaseModel):
    name: str
    fees: int
    tid: int | None = None
    joining_date: date
class MemberUpdate(BaseModel):
    name: str | None = None
    fees: int | None = None
    tid: int | None = None
class Trainer(BaseSchema):
    tid: int
    name: str
    salary: int
    email: str

class TrainerCreate(BaseSchema):
    name: str
    salary: int
    email: str
class Membership(BaseSchema):
    membership_id: int
    member_id: int
    start_date: date
    end_date: date
    status: str

class MembershipCreate(BaseModel):
    member_id: int
    start_date: date
    end_date: date
    status: str = "Active"

class MembershipRenew(BaseModel):
    new_end_date: date
    status: str = "Active"
class Payment(BaseSchema):
    pid: int
    member_id: int
    amount: int
    date: date
    status: str

class PaymentCreate(BaseSchema):
    member_id: int
    amount: int
    date: date
    status: str

class Attendance(BaseSchema):
    attendance_id: int
    member_id: int
    date: date
    status: str

class AttendanceHistory(BaseSchema):
    attendance_id: int
    date: date
    status: str

class WorkoutSchedule(BaseSchema):
    schedule_id: int
    member_id: int
    trainer_id: int
    workout_details: str

class WorkoutScheduleCreate(BaseSchema):
    member_id: int
    trainer_id: int
    workout_details: str