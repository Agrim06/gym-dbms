from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas import Member, Trainer, Membership, Payment


router = APIRouter(prefix="/gym")

