#Main FastAPI app file
from typing import Union, TYPE_CHECKING
from fastapi import FastAPI, Depends
import sqlalchemy.orm.session as Session

from services import get_db
from models import User
import schemas as Schemas

#Type checking is a way to tell the Python interpreter to check the types of your code.
if TYPE_CHECKING:
    from sqlalchemy.orm import Session

app = FastAPI(title="FastAPI, Docker, OAuth2, and PostgreSQL exercise")

#standard Hello World route
@app.get("/")
def read_root():
    return {"Hello": "World"}

#CRUD OPERATIONS

#Create
#Create a new user
@app.post("/")
async def create_user(user: Schemas.CreateUser, db: Session = Depends(get_db)):
    createUser = User(username=user.username, email=user.email)
    db.add(createUser)
    db.commit()
    print("User created")
    return user

#Read
#get a user by id
@app.get("/api/users/id/{user_id}")
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    try:
        return db.query(User).filter(User.id == user_id).first()
    except:
        return "User not found or Internal Server Error"

#Update
#Update a user by id
@app.put("/api/users/id/{user_id}")
async def update_user_by_id(user_id: int, user: Schemas.CreateUser, db: Session = Depends(get_db)):
    try:
        db.query(User).filter(User.id == user_id).update({"username": user.username, "email": user.email})
        db.commit()
        return "User updated"
    except:
        return "User not found or Internal Server Error"

#Delete
#Delete a user by id
@app.delete("/api/users/id/{user_id}")
async def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    try:
        db.query(User).filter(User.id == user_id).delete()
        db.commit()
        return "User deleted"
    except:
        return "User not found or Internal Server Error"

#get every user in the database
@app.get("/api/users/all/")
async def get_all_users(db: Session = Depends(get_db)):
    try:
        return db.query(User).all()
    except:
        return "Internal Server Error"

#I love GitHub Autopilot