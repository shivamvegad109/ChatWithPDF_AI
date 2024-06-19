import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Establish a connection to the database
def connection_to_mysql():
    try:
        conn = mysql.connector.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME')  # Add database if required
        )
        if conn.is_connected():
            print("Connection to MySQL database was successful")
            return conn
        else:
            print("Failed to connect to MySQL database")
            return None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

conn = connection_to_mysql()
print("connected successfully")