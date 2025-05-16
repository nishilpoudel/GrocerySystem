from fastapi import APIRouter
from fastapi import Depends, HTTPException
from psycopg2.extensions import connection as Connection
import psycopg2
from ..db import get_db
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from ..models import UserItem,User
from ..oauth2 import get_current_user




router = APIRouter()

@router.get("/user-items", response_model=List[UserItem])
def get_user_items(current_user = Depends(get_current_user), db : Connection = Depends(get_db)):
    
    try : 
        user_id = current_user.id
        cur = db.cursor()
        cur.execute("""SELECT i.name, i.price, i.description, i.is_organic FROM items AS i
                    JOIN user_items AS ui on ui.item_id = i.id 
                    WHERE ui.user_id = %s """, (user_id,))
        items = cur.fetchall()
        cur.close()
        return items
    except psycopg2.Error as e:
        return {"Error" : str(e)}
    


