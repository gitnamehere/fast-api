from fastapi import FastAPI, Depends, HTTPException, status
import sqlalchemy.orm.session as Session
from pydantic import BaseModel

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from database import SessionLocal, engine, get_db
import services as Services
from models import User
from schemas import Token, TokenData
from datetime import datetime, timedelta

#Generate a new secret key with the following command:
#openssl rand -hex 32
SECRET_KEY = "SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

#Gets a password hash from a plaintext password
def get_password_hash(password: str):
    return pwd_context.hash(password)

#Verify password
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

#Authenticate user based on username and password
def authenticate_user(username: str, password: str, db: Session):
    user = Services.get_user_by_username(username, db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

#Generates a new access token
def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"iat": datetime.utcnow(),"exp": expire,})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

#Get current user based on the access token. 
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = Services.get_user_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

#Obtain an access token from successful login
def login_for_access_token(form_data: OAuth2PasswordRequestForm, db: Session):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(
        data={"sub": user.id, "username": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}