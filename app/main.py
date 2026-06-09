from fastapi import FastAPI
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from models import Base, User

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "UP"}

@app.get("/users")
def get_users():

    db = SessionLocal()

    users = db.query(User).all()

    return [
        {
            "id": u.id,
            "name": u.name
        }
        for u in users
    ]
