from fastapi import APIRouter, Response
from fastapi import Depends, HTTPException, status
from psycopg2.extensions import connection as Connection
import psycopg2
from ..db import get_db
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from ..models import User
from ..utils import verify_password
from ..oauth2 import create_access_token, create_refresh_token


router = APIRouter()

@router.post("/login")
def login(response : Response, user_credentials: OAuth2PasswordRequestForm = Depends(), db : Connection = Depends(get_db)):
    try:
        cur = db.cursor()
        cur.execute("""SELECT * FROM users WHERE email = %s""", (user_credentials.username,))
        user_data = cur.fetchone()
        if not user_data:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Invalid Credentials")
        cur.close()    
        user = User(**user_data)    
        if not verify_password(user_credentials.password, user.hashed_password):
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
        
        access_token = create_access_token(data= {"user_id" : user.id})
        refresh_token = create_refresh_token(data={"user_id" : user.id})

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite='lax',         
        )
        return {"access_token": access_token, "token_type": "bearer"}
    
    except psycopg2.Error as e:
        return {"Error", str(e)}