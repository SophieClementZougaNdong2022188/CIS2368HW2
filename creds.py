class myCreds:
    hostname = "cis2368database.cqznz0sza3gn.us-east-1.rds.amazonaws.com"
    username = "admin"
    password = "password"
    database = "cis2368db1"
    
import mysql.connector
from mysql.connector import Error
 
def connect_to_mysql():
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host='cis2368database.cqznz0sza3gn.us-east-1.rds.amazonaws.com',  # Replace with your MySQL host, e.g., '127.0.0.1'
            user='admin',  # Replace with your MySQL username
            password='password',  # Replace with your MySQL password
            database='cis2368db1'  # Replace with your MySQL database name
        )
 
        if connection.is_connected():
            db_info = connection.get_server_info()
            print("Connected to MySQL Server version", db_info)
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print("You're connected to the database:", record)
 
    except Error as e:
        print("Error while connecting to MySQL", e)
 
    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
 
# Run the connection test
connect_to_mysql()