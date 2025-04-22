from fastapi import Depends, APIRouter, HTTPException
from psycopg2.extensions import connection as Connection
import psycopg2

from .. models import User, UserCreate, UserID
from ..db import get_db
from typing import List
from ..utils import hash


router = APIRouter()



@router.get("/users", response_model= List[User])
def get_users(db : Connection = Depends(get_db)):
    try : 
        cur = db.cursor()
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        cur.close()
        return users
    except psycopg2.Error as e:
        print("Could not get users", str(e))



@router.post("/create-user")
def create_user(user : UserCreate, db : Connection = Depends(get_db)):
    try: 
        hashing_password = hash(user.hashed_password)
        user.hashed_password = hashing_password
        cur = db.cursor()
        cur.execute("""INSERT INTO users(first_name, last_name, email, hashed_password)
        VALUES(%s,%s,%s,%s) RETURNING * """ , 
        (user.first_name, user.last_name, user.email, user.hashed_password))
        new_user = cur.fetchone()
        db.commit()
        cur.close()
        return new_user
    except psycopg2.Error as e :
        print("Error", str(e))


@router.get("/user/{id}", response_model= UserID)
def get_user_id(id : int, db : Connection = Depends(get_db)):
    cur = db.cursor()
    cur.execute("""SELECT id, first_name, last_name, email FROM users WHERE id = %s""", (id,))
    user = cur.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id :{id} not found ")
    cur.close()
    return user
