from fastapi import FastAPI, Depends, Form, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extensions import connection as Connection
from datetime import date
from typing import List, Optional
from psycopg2.extras import RealDictCursor
from fastapi.staticfiles import StaticFiles
from backend import crud
from fastapi.responses import FileResponse
import os
from dotenv import load_dotenv
from fastapi.responses import RedirectResponse
from .models import User, UserCreate, UserID, UserLogin
from .utils import hash, verify_password
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")




def get_db():
    #get db connection
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory= RealDictCursor)
        yield conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        raise
    finally:
        if conn:
            conn.close()

class Item(BaseModel):
    name : str
    default_price : float
    id : int 
    is_organic : Optional[bool]
    description : Optional[str]
    image_url : Optional[str]

class UserItem(BaseModel):
    user_id : Optional[int]
    item_id: Optional[int]
    price : float
    quantity : int
    exp_date : Optional[date]
    


app = FastAPI()

app.mount("/static",StaticFiles(directory="frontend", html=True), name="static")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/security")
async def security(token : Annotated [str, Depends(oauth2_scheme)]):
    return {"token" : token}


@app.get("/")
def read_index():
    return FileResponse("frontend/landing.html")

@app.get("/items",response_model= List[Item])
def get_items(db : Connection = Depends(get_db)):
    try: 
        cur = db.cursor()
        cur.execute("SELECT * FROM items")
        items = cur.fetchall()
        cur.close()
        return items
    except psycopg2.Error as e:
        return {"Error" : str(e)}


## SQL join is incomplete. (Need to look at db tables and figure out how to query a user item )
@app.get("/user-items", response_model=List[UserItem])
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

@app.get("/items/{id}", response_model= Item)
def get_item(id, db : Connection = Depends(get_db)):
    cur = db.cursor()
    id = cur.execute("""SELECT * FROM items WHERE id = %s""", (id,))
    id = cur.fetchone()
    if not id:
        print("Error")
    item = Item(**id)
    return item

@app.get('/create-item')
def read_create_form():
    return FileResponse("frontend/index.html")



@app.post("/create", response_model= Item)
def create_item_endpoint(
    name : str = Form(...),
    price : float = Form(...),
    quantity : int = Form(...),
    organic : str = Form(...),
    exp_date : str = Form(...),
    db : Connection = Depends(get_db)
):
    #convert the organic field to a boolean value 
    is_organic = True if organic.lower() == "yes" else False

    try:    
        new_item = crud.create_item(db, name, price,quantity,is_organic, exp_date)
        if not new_item:
            raise HTTPException(status_code=400, detail= "Item creation failed")
        return RedirectResponse("/", status_code= 303 )
    except Exception as e:
        print("Error : ", e)
        raise HTTPException(status_code=500, detail="Internal Server Error ")

@app.delete('/delete_item/{id}')
def delete_item(id, db : Connection = Depends(get_db)):
    cur = db.cursor()
    cur.execute("DELETE FROM items where id = %s", (id))
    db.commit()
    cur.close()
    return {f"Success : Item of id {id} was deleted"}



@app.get("/users", response_model= List[User])
def get_users(db : Connection = Depends(get_db)):
    try : 
        cur = db.cursor()
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        cur.close()
        return users
    except psycopg2.Error as e:
        print("Could not get users", str(e))



@app.post("/create-user")
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
        cur.close
        return new_user
    except psycopg2.Error as e :
        print("Error", str(e))


@app.get("/user/{id}", response_model= UserID)
def get_user_id(id : int, db : Connection = Depends(get_db)):
    cur = db.cursor()
    cur.execute("""SELECT id, first_name, last_name, email FROM users WHERE id = %s""", (id,))
    user = cur.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id :{id} not found ")
    cur.close()
    return user



@app.post("/login")
def login(user_credentials:UserLogin, db : Connection = Depends(get_db)):
    try:
        cur = db.cursor()
        cur.execute("""SELECT * FROM users WHERE email = %s""", (user_credentials.email,))
        user_data = cur.fetchone()
        if not user_data:
            raise HTTPException(status_code=404, detail= "Invalid Credentials")
        cur.close()    
        user = User(**user_data)    
        if not verify_password(user_credentials.hashed_password, user.hashed_password):
            raise HTTPException(status_code=404, detail="Invalid Credentials")
        return {"token" : "token created"}
    
    except psycopg2.Error as e:
        return {"Error", str(e)}

 


        





# when a user adds an item to their list 
# first we check if the item name exists in the db already 
# if so we add it to their list 
# if not we create a new item and then add it to their list 

