from fastapi import FastAPI
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import User

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "UP"}


@app.get("/users")
def get_users():
    db = SessionLocal()
    users = db.query(User).all()

    return [{"id": u.id, "name": u.name} for u in users]
