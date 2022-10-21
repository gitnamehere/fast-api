#Main FastAPI app file
from http.client import HTTPException
from typing import Union, TYPE_CHECKING
from fastapi import FastAPI, Depends, HTTPException
import sqlalchemy.orm.session as Session
from pydantic import BaseModel

import services as Services
from models import User
import schemas as Schemas
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "f894fe55f80b0f9dfc01b84d26a6d88020bb0e707f1a84159e19142020efe6e5"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
TOKEN_SECRET = "secret"

#Type checking is a way to tell the Python interpreter to check the types of your code.
if TYPE_CHECKING:
    from sqlalchemy.orm import Session

app = FastAPI(title="FastAPI, Docker, OAuth2, and PostgreSQL exercise")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


@app.post("/token", response_model=Schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(Services.get_db)):
    user = authenticate_user(db, form_data.username)


def authenticate_user(username: str, password: str,db: Session = Depends(Services.get_db)):
    user = Services.get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/token", response_model=Schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(Services.get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/items")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}

#standard Hello World route
@app.get("/")
def read_root():
    return {"Hello": "World"}

#CRUD OPERATIONS

#Create
#Create a new user
@app.post("/api/users")
async def create_user(user: Schemas.CreateUser, db: Session = Depends(Services.get_db)):
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