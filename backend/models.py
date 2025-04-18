from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Item(BaseModel):
    id : int 
    name : str
    default_price : int
    is_organic : Optional[bool]
    description : Optional[str]
    image_url : Optional[str]


class UserItem(BaseModel):
    first_name : str
    last_name : str
    price : int 
    quantity : int
    note : Optional[str]
    exp_date : Optional[datetime]
    is_organic : Optional[bool]
    image_url : Optional[str]


class User(BaseModel):
    id : int 
    first_name : str
    last_name : str
    email : str
    hashed_password : str
    created_at : datetime

class UserCreate(BaseModel):
    first_name : str
    last_name : str
    email : str
    hashed_password : str

class UserID(BaseModel):
    id: int 
    first_name : str
    last_name : str
    email : str

class UserLogin(BaseModel):
    email : str
    hashed_password : str


class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[str] = None



