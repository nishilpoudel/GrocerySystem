from fastapi import APIRouter
from fastapi import Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from psycopg2.extensions import connection as Connection
import psycopg2
from ..db import get_db
from ..crud import create_item
from typing import List
from ..models import Item, ItemCreate, DisplayItem
from ..oauth2 import get_current_user
from ..models import TokenData


router = APIRouter()


@router.get("/items",response_model= List[DisplayItem])
def get_items(current_user = Depends(get_current_user), db : Connection = Depends(get_db)):
    try: 
        user_id = current_user.id
        cur = db.cursor()
        cur.execute("""SELECT i.name, i.price, i.description, i.is_organic, i.image_url
                    FROM user_items AS ui
                    JOIN items AS i
                    ON ui.item_id = i.id
                    WHERE ui.user_id = %s""", (user_id,))
        items = cur.fetchall()
        cur.close()
        return items
    except psycopg2.Error as e:
        return {"Error" : str(e)}
    

@router.get("/items/{id}", response_model= Item)
def get_item(id, db : Connection = Depends(get_db)):
    cur = db.cursor()
    id = cur.execute("""SELECT * FROM items WHERE id = %s""", (id,))
    id = cur.fetchone()
    if not id:
        print("Error")
    item = Item(**id)
    return item


@router.delete('/delete_item/{id}')
def delete_item(id, db : Connection = Depends(get_db)):
    cur = db.cursor()
    cur.execute("DELETE FROM items where id = %s", (id,))
    db.commit()
    cur.close()
    return {f"Success : Item of id {id} was deleted"}


@router.post("/create", response_model= Item)
def create_item_endpoint(
    payload : ItemCreate,
    db : Connection = Depends(get_db),
    current_user  = Depends(get_current_user)
):
    try:    
        new_item = create_item(db, payload.name, payload.price,payload.description,payload.is_organic, current_user.id)
        if not new_item:
            raise HTTPException(status_code=400, detail= "Item creation failed")
    
        return RedirectResponse("/", status_code= 303 )
    except Exception as e:
        print("Error : ", e)
        raise HTTPException(status_code=500, detail="Internal Server Error ")
        
        
    
