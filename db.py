import psycopg2
from psycopg2 import OperationalError

#Step 01 : Connection to postgres
def get_connection():
    try:
        conn = psycopg2.connect(
            host = "localhost",
            database = "DEV",
            user = "postgres",
            password = "qwerty",
            port = "5432"
        )
        return conn
    except OperationalError as e:
        print(f"Error connecting DB DEV : {e}")
        return None