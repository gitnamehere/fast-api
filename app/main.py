#Main FastAPI app file
from http.client import HTTPException
from typing import Union, TYPE_CHECKING
from fastapi import FastAPI, Depends, HTTPException
import sqlalchemy.orm.session as Session

import services as Services
from models import User
import schemas as Schemas

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

TOKEN_SECRET = "secret"

#Type checking is a way to tell the Python interpreter to check the types of your code.
if TYPE_CHECKING:
    from sqlalchemy.orm import Session

app = FastAPI(title="FastAPI, Docker, OAuth2, and PostgreSQL exercise")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#standard Hello World route
@app.get("/")
def read_root():
    return {"Hello": "World"}

#CRUD OPERATIONS

#Create
#Create a new user
@app.post("/api/users")
async def create_user(user: Schemas.CreateUser, db: Session = Depends(Services.get_db)):
    db_user = Services.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken, or Email already registered")
    db_user = Services.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken, or Email already registered")
    return Services.create_user(db=db, user=user)

#Read
#get a user by id
@app.get("/api/users/id/{user_id}")
async def get_user_by_id(user_id: int, db: Session = Depends(Services.get_db)):
    db_user = Services.get_user_by_id(user_id, db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

#get every user in the database
@app.get("/api/users/all/")
async def get_all_users(page: int = 0, limit: int = 100, db: Session = Depends(Services.get_db)):
    return Services.get_all_users(db, page=page, limit=limit)

#Update
#Update a user by id
@app.put("/api/users/id/{user_id}")
async def update_user_by_id(user_id: int, user: Schemas.CreateUser, db: Session = Depends(Services.get_db)):
    db_user = Services.get_user_by_id(user_id, db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return Services.update_user_by_id(user_id, user, db)

#Delete
#Delete a user by id
@app.delete("/api/users/id/{user_id}")
async def delete_user_by_id(user_id: int, db: Session = Depends(Services.get_db)):
    db_user = Services.get_user_by_id(user_id, db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return Services.delete_user_by_id(user_id, db)

#I love GitHub Autopilot