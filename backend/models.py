import mysql.connector
from database import get_connection

# Create Users Table if not exists
def create_users_table():
    try:
        conn = get_connection()
        if conn is None:
            print("No database connection. Table creation skipped.")
            return
        
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users( 
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL
            )                   
        """)
        
        conn.commit()
        conn.close()
        print("User table created (if not exists)")
    
    except Exception as e:
        print(f"Error creating user table: {e}")    

# Call this function when the server starts
create_users_table()
