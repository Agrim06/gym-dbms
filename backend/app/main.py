from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import engine, Base
from . import models
from .api import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables verified/created successfully.")
    except Exception as e:
        print(f"Warning: Could not connect to database on startup: {e}")
    yield

app = FastAPI(
    title="Gym Management System",
    description="DBMS Project API for managing members, trainers, memberships, payments, attendance, and workout schedules.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router)
