from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi import Cookie
from ..oauth2 import verify_refresh_token, create_access_token


router = APIRouter()

@router.post("/refresh")
def refresh_token(refresh_token : str = Cookie(None, title="Refresh Token")):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail="Could not validate refresh token",
                                          headers={"WWW-Authentication":"Bearer"},)
    if not refresh_token:
        raise credentials_exception
    
    token_data = verify_refresh_token(refresh_token,credentials_exception)
    new_access = create_access_token({"user_id": token_data.id})

    return {"access_token" : new_access, "token_type":"bearer"}