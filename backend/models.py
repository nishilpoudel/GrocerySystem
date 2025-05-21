from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Item(BaseModel):
    id : int 
    name : str
    price : float
    is_organic : Optional[bool]
    description : Optional[str]

class DisplayItem(BaseModel):
    name : str
    price : float
    description : str
    is_organic : Optional[bool]




class ItemCreate(BaseModel):
    name : str
    price : float
    is_organic : Optional[bool]
    description : Optional[str]


class UserItem(BaseModel):

    id : int
    name : str
    price : float
    description : str
    is_organic : bool

    # first_name : str
    # last_name : str
    # price : int 
    # quantity : int
    # note : Optional[str]
    # exp_date : Optional[datetime]
    # is_organic : Optional[bool]
    # image_url : Optional[str]


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
    id : Optional[int] = None



