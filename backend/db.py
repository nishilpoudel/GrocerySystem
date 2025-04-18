import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os


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
