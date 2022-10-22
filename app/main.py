#Main FastAPI app file
from http.client import HTTPException
from typing import Union, TYPE_CHECKING
from fastapi import FastAPI, Depends, HTTPException, status
import sqlalchemy.orm.session as Session
from pydantic import BaseModel
import database as Database

import services as Services
from models import User
import schemas as Schemas
from datetime import datetime, timedelta

import auth as Auth
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "151087c62cbc70bb668cdedf5dab5452e3d79ffdd55317732450dcecc60804f7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(title="FastAPI, Docker, OAuth2, and PostgreSQL exercise")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

@app.post("/api/token", response_model=Schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(Database.get_db)):
    user = Auth.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = Auth.create_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/")
async def read_users_me(current_user: User = Depends(Auth.get_current_user)):
    return current_user

#standard Hello World route
@app.get("/")
def read_root():
    return {"Hello": "World"}

#CRUD OPERATIONS

#Create
#Create a new user
@app.post("/api/users")
async def create_user(user: Schemas.CreateUser, db: Session = Depends(Database.get_db)):
    db_user = Services.get_user_by_email(email=user.email, db=db)
    if db_user != None:
        raise HTTPException(status_code=400, detail="Username already taken, or Email already registered")
    db_user = Services.get_user_by_username(username=user.username, db=db)
    if db_user != None:
        raise HTTPException(status_code=400, detail="Username already taken, or Email already registered")
    return Services.create_user(db=db, user=user)

#Read
#get a user by id
@app.get("/api/users/id/{user_id}")
async def get_user_by_id(user_id: int, db: Session = Depends(Database.get_db)):
    db_user = Services.get_user_by_id(user_id, db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

#get every user in the database
@app.get("/api/users/all/")
async def get_all_users(page: int = 0, limit: int = 100, db: Session = Depends(Database.get_db)):
    return Services.get_all_users(db, page=page, limit=limit)

#Update
#Update a user by id
@app.put("/api/users/id/{user_id}")
async def update_user_by_id(user_id: int, user: Schemas.CreateUser, db: Session = Depends(Database.get_db)):
    db_user = Services.get_user_by_id(user_id, db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return Services.update_user_by_id(user_id, user, db)

#Delete
#Delete a user by id
@app.delete("/api/users/id/{user_id}")
async def delete_user_by_id(user_id: int, db: Session = Depends(Database.get_db)):
    db_user = Services.get_user_by_id(user_id, db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return Services.delete_user_by_id(user_id, db)

#I love GitHub Autopilot