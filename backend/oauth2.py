import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from .models import TokenData
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
import os
from dotenv import load_dotenv

load_dotenv()



oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRATION = int(os.getenv("ACCESS_TOKEN_EXPIRATION"))
REFRESH_TOKEN_EXPIRATION = int(os.getenv("REFRESH_TOKEN_EXPIRATION"))


def create_access_token(data : dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes= ACCESS_TOKEN_EXPIRATION)
    to_encode.update({"exp": expire, "type" : "access"})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data : dict, expires_delta : timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRATION)
    to_encode.update({"exp":expire, "type" : "refresh"})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token : str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        if payload.get("type") != "access" or payload.get("user_id") is None:
            raise credentials_exception
        return TokenData(id=payload["user_id"])
    except(InvalidTokenError, KeyError):
        raise credentials_exception
    
def verify_refresh_token(token : str, credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        if payload.get("type") != "refresh" or payload.get("user_id") is None:
            raise credentials_exception
        return TokenData(id=payload["user_id"])
    except(InvalidTokenError, KeyError):
        raise credentials_exception


def get_current_user(token : str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail= f"Could not validate credentials",
                                          headers={"WWW-Authenticate":"Bearer"},) 
    return verify_access_token(token, credentials_exception)