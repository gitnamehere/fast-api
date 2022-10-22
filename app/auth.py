from fastapi import FastAPI, Depends, HTTPException
import sqlalchemy.orm.session as Session
from pydantic import BaseModel

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

import database as Database
from database import SessionLocal, engine
import services as Services
from models import User
from schemas import Token, TokenData
from datetime import datetime, timedelta

SECRET_KEY = "151087c62cbc70bb668cdedf5dab5452e3d79ffdd55317732450dcecc60804f7"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str, db: Session):
    user = Services.get_user_by_username(username, db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = Services.get_user_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user