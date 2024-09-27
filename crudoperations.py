import mysql.connector
from mysql.connector import Error
 
import creds

from sql import DBconnection

mycreds = creds.myCreds()
mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)