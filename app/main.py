from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    email: str

#hardcoded data for testing
users = {
    1: {
        "username": "John Doe",
        "age": 30,
    },
    2: {
        "username": "Jane Doe",
        "age": 27,
    }
}

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/users/{user_id}")
def read_user(user_id: int):
    return users[user_id]