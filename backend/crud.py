from psycopg2.extensions import connection as Connection 
from datetime import datetime

def create_item(db : Connection, name : str, price : float, quantity : int, is_organic : bool, exp_date : str ): 
    cur = db.cursor()
    try :
        #convert the date string to a date object 
        exp_date_parsed = datetime.strptime(exp_date, "%Y-%m-%d").date() if exp_date else None
        cur.execute("""INSERT INTO items(name, price, is_organic, exp_date, quantity) 
                    VALUES(%s, %s, %s, %s, %s) RETURNING * """, (name,price, is_organic, exp_date_parsed, quantity))
        
        new_item = cur.fetchone()
        db.commit()
        return new_item
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cur.close()



