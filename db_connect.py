import mysql.connector 

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Luck@#956",  # Change to your MySQL password
        database="ecommerce_db"
    )
