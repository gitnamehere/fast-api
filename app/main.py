#Main FastAPI app file
from typing import Union, TYPE_CHECKING
from fastapi import FastAPI, Depends
import sqlalchemy.orm.session as Session

import services as Services
import models as Models
import schemas as Schemas

#Type checking is a way to tell the Python interpreter to check the types of your code.
if TYPE_CHECKING:
    from sqlalchemy.orm import Session

app = FastAPI(title="FastAPI, Docker, OAuth2, and PostgreSQL exercise")

#standard Hello World
@app.get("/")
def read_root():
    return {"Hello": "World"}

#Create a new user
@app.post("/")
async def create_user(user: Schemas.CreateUser, db: Session = Depends(Services.get_db)):

    #Note: Integrate into services.py later
    createUser = Models.User(username=user.username, email=user.email)
    db.add(createUser)
    db.commit()
    print("User created")
    return user

#get a user by id
@app.get("/users/id/{user_id}")
async def get_user_by_id(user_id: int, db: Session = Depends(Services.get_db)):
    try:
        return db.query(Models.User).filter(Models.User.id == user_id).first()
    except:
        return "User not found or Internal Server Error"

#get every user in the database
@app.get("/users/all/")
async def get_all_users(db: Session = Depends(Services.get_db)):
    try:
        return db.query(Models.User).all()
    except:
        return "Internal Server Error"