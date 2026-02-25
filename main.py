from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///./users.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# SQLAlchemy Model
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)

Base.metadata.create_all(bind=engine)

# Pydantic Schema
class User(BaseModel):
    id: int
    name: str
    email: str

@app.get("/")
def home():
    return {"message": "API is working with Database"}

@app.post("/users")
def create_user(user: User):
    db = SessionLocal()
    db_user = UserDB(id=user.id, name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.close()
    return {"message": "User added"}

@app.get("/users")
def get_users():
    db = SessionLocal()
    users = db.query(UserDB).all()
    db.close()
    return users

@app.get("/users/{user_id}")
def get_user(user_id: int):
    db = SessionLocal()
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    db.close()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: User):
    db = SessionLocal()
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    user.name = updated_user.name
    user.email = updated_user.email
    db.commit()
    db.close()
    return {"message": "User updated"}

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    db = SessionLocal()
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    db.close()
    return {"message": "User deleted"}


port = int(os.environ.get("PORT", 8000))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port)