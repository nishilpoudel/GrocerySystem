from fastapi import APIRouter
from fastapi import Depends, HTTPException
from psycopg2.extensions import connection as Connection
import psycopg2
from ..db import get_db
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
    


