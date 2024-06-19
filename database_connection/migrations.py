from database_connection.connectionN import connection_to_mysql
import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

conn = connection_to_mysql()

# Function for creating database
def create_database(conn):
    if conn is None:
        print("Connection is not established.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DATABASE_NAME')}")
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")
    finally:
        cursor.close()

# Function for USE database
def use_database(conn):
    if conn is None:
        print("Connection is not established.")
        return
    try:
        cursor = conn.cursor()
        cursor.execute(f"USE {os.getenv('DATABASE_NAME')}")
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error using database: {err}")
    finally:
        cursor.close()

# Function for creating table
def create_table(conn):
    if conn is None:
        print("Connection is not established.")
        return

    use_database(conn)
    try:
        cursor = conn.cursor()
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {os.getenv('TABLE_NAME')} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                question LONGTEXT,
                answer LONGTEXT,
                file_name LONGTEXT
            )
        ''')
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    finally:
        cursor.close()

# Function for inserting data into the QA table
def insert_into_qa(question, answer, file_name):
    if conn is None:
        print("Connection is not established.")
        return "Failed to add into table due to connection issue"

    use_database(conn)

    try:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO {} (question, answer, file_name) VALUES (%s, %s, %s)'''.format(os.getenv('TABLE_NAME')), (question, answer, file_name))
        conn.commit()
        return "added successfully into table"
    except mysql.connector.Error as err:
        print(f"Error inserting into table: {err}")
        return "Failed to add into table"
    finally:
        cursor.close()


