from fastapi import APIRouter
from fastapi import Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from psycopg2.extensions import connection as Connection
import psycopg2
from ..db import get_db
from ..crud import create_item
from typing import List

from ..models import Item


router = APIRouter()


@router.get("/items",response_model= List[Item])
def get_items(db : Connection = Depends(get_db)):
    try: 
        cur = db.cursor()
        cur.execute("SELECT * FROM items")
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
        new_item = create_item(db, name, price,quantity,is_organic, exp_date)
        if not new_item:
            raise HTTPException(status_code=400, detail= "Item creation failed")
        return RedirectResponse("/", status_code= 303 )
    except Exception as e:
        print("Error : ", e)
        raise HTTPException(status_code=500, detail="Internal Server Error ")