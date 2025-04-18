from fastapi import APIRouter
from fastapi import Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from psycopg2.extensions import connection as Connection
import psycopg2
from ..db import get_db
from ..crud import create_item
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from ..models import UserItem,User
from ..utils import verify_password
from ..oauth2 import create_access_token


router = APIRouter()

# SQL join is incomplete. (Need to look at db tables and figure out how to query a user item )
@router.get("/user-items", response_model=List[UserItem])
def get_user_items(db : Connection = Depends(get_db)):
    try : 
        cur = db.cursor()
        cur.execute("""SELECT users.first_name, last_name, user_items.price, user_items.quantity, user_items.note, user_items.exp_date
        FROM users """)
        items = cur.fetchall()
        cur.close()
        return items
    except psycopg2.Error as e:
        return {"Error" : str(e)}
    


@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db : Connection = Depends(get_db)):
    try:
        cur = db.cursor()
        cur.execute("""SELECT * FROM users WHERE email = %s""", (user_credentials.username,))
        user_data = cur.fetchone()
        if not user_data:
            raise HTTPException(status_code=404, detail= "Invalid Credentials")
        cur.close()    
        user = User(**user_data)    
        if not verify_password(user_credentials.password, user.hashed_password):
            raise HTTPException(status_code=404, detail="Invalid Credentials")
        
        access_token = create_access_token(data= {"user_id" : user.id})
        return {"access token" : access_token, "token_type" : "bearer"}
    
    except psycopg2.Error as e:
        return {"Error", str(e)}