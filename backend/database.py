import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database Connection
def get_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        print("Database connection successful")
        return conn
    except mysql.connector.Error as err:
        print(f"Database connection failed: {err}")
        return None