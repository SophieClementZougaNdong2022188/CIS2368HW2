import mysql.connector
from mysql.connector import Error
 
# Function to establish a connection to the database
def DBconnection(hostname, uname, pwd, dbname):
    mycon = None
    try:
        mycon = mysql.connector.connect(
            host=hostname,
            user=uname,
            password=pwd,
            database=dbname
        )
        if mycon.is_connected():
            print("MySQL Database connection was successful")
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    return mycon
# Execute qquery function to read the rows from table
def execute_read_query(con,sql):
    mycursor = con.cursor(dictionary=True)
    rows = None
    try:
        sql_select = "SELECT * FROM users1"
        mycursor.execute(sql_select)
        userrows = mycursor.fetchall()
        return userrows
    except Error as e:
        print("Error is: ", e)
 
#Execute query function to insert the rows into table
def execute_update_query(con, sql):
    mycursor = con.cursor()
    try:
        mycursor.execute(sql)
        con.commit()
        print("DB update successful")
    except Error as e:
        print("Error is : ". e)