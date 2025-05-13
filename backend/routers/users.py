from fastapi import Depends, APIRouter, HTTPException, status, Response
from fastapi.responses import JSONResponse
from psycopg2.extensions import connection as Connection
import psycopg2

from .. models import User, UserCreate, UserID
from ..db import get_db
from typing import List
from ..utils import hash
from ..oauth2 import create_access_token, verify_access_token, create_refresh_token


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
def create_user(response : Response, payLoad : UserCreate, db : Connection = Depends(get_db)):
    try: 
        hashing_password = hash(payLoad.hashed_password)
        payLoad.hashed_password = hashing_password
        cur = db.cursor()
        cur.execute("""INSERT INTO users(first_name, last_name, email, hashed_password)
        VALUES(%s,%s,%s,%s) RETURNING * """ , 
        (payLoad.first_name, payLoad.last_name, payLoad.email, payLoad.hashed_password))
        new_user = cur.fetchone()
        id = new_user['id']
        db.commit()
        cur.close()
        access_token = create_access_token(data= {"user_id":id})
        refresh_token = create_refresh_token(data={"user_id":id})
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
        )

        

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content= {"access_token": access_token, "token_type": "bearer"},
        )
        
        
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
