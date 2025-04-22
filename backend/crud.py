from psycopg2.extensions import connection as Connection 
from datetime import datetime

def create_item(db : Connection, name : str, price : float, description : str, is_organic : bool , image_url : str, user_id : int): 
    cur = db.cursor()
    try :
        cur.execute("""INSERT INTO items(name, price, description, is_organic, image_url) 
                    VALUES(%s, %s, %s, %s, %s) RETURNING * """, (name,price, description, is_organic, image_url))
        
        new_item = cur.fetchone()
        item_id = new_item['id']

        cur.execute("""INSERT INTO user_items(user_id, item_id) VALUES (%s,%s)""", (user_id,item_id))
        
        db.commit()
        return new_item
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cur.close()



