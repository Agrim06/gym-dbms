from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date

class Member(BaseModel):
    uid : int
    name : str
    fees : int
    tid : int
    joining_date : date

class Trainer(BaseModel):
    tid : int
    name : str
    salary : int
    email : str

class Membership(BaseModel):
    membership_id: int
    member_id : int
    start_date : date
    end_date : date
    status : str

class Payment(BaseModel):
    pid : int
    membership_id : int
    amount : int
    date : date
    status : str
