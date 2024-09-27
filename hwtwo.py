#database can't connect for some reason, when it does place the necessary information
#commit at least three times to GitHub and turn in the link
#/api/householditems get, post, put , delete
from flask import Flask
from flask import jsonify, request
from sql import DBconnection, execute_read_query, execute_update_query
import mysql.connector
from mysql.connector import Error
import creds

app = Flask(__name__)
app.config['DEBUG'] = True
#try switching the database and the host name? To see if it will connect now
def DBconnection(hostname, username, pwd, dbname):
    try:
        # Establishing connection to the MySQL database
        connection = mysql.connector.connect(
            host=hostname,
            user=username,
            password=pwd,
            database=dbname
        )
        if connection.is_connected():
            print("MySQL Database connection was successful")
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None
#might have to leave the function as is and get rid of the try and except clause because that might be the issue for some reason
#function below is just to make sure it runs
def execute_update_query(con, sql):
    mycursor = con.cursor()
    try:
        mycursor.execute(sql)
        con.commit()
        print("DB update successful")
    except Error as e:
        print("Error is : ". e)


@app.route('/', methods=['GET'])
def home():
    return "<h1> Household Items List </h1>"

householditemslist = [
    {
        "ID":1,
        "NAME": "CHAIR",
        "CATEGORY": "LIVING_ROOM",
        "QUANTITY": 2,
        "STATUS": "USED"
    },
    {
        "ID":2,
        "NAME": "COUCH",
        "CATEGORY": "LIVING_ROOM",
        "QUANTITY": 1,
        "STATUS": "NEW"
    },
    {
        "ID":3,
        "NAME": "TABLE",
        "CATEGORY": "LIVING_ROOM",
        "QUANTITY": 1,
        "STATUS": "NEW"
    },
    {
        "ID":4,
        "NAME": "STOVE",
        "CATEGORY": "KITCHEN",
        "QUANTITY": 1,
        "STATUS": "USED"
    },
    {
        "ID":5,
        "NAME": "FRIDGE",
        "CATEGORY": "KITCHEN",
        "QUANTITY": 1,
        "STATUS": "USED"
    }
]


# if __name__ == '__main__':
#     app.run(debug = True)
    
    
@app.route('/api/householditems/all', methods = ['GET'])
def allhouseholditems():
    return jsonify(householditemslist)

@app.route('/api/householditems/single', methods=['GET'])
def singlehouseholditem():
    # request.args consists of parameter arguments passed in request. 
    # Below code retriving parameter 'id' from request arguments 
    if 'ID' in request.args:
        ID = int(request.args['ID'])
    else:
        return "Error: No ID found"

    for item in householditemslist:
        if item['ID']==ID:
            return(item)
        
@app.route('/householditems/update', methods=['POST']) #do I put api at the beginning of the address or no?
def updatehouseholditems():
    userinput = request.get_json()
    if not userinput:
        return "Invalid input", 400

    newid = userinput.get('ID')
    newname = userinput.get('NAME')
    newcategory = userinput.get('CATEGORY')
    newquantity = userinput.get('QUANTITY')
    newstatus = userinput.get('STATUS')

    if not newid or not newname or not newcategory or not newquantity or not newstatus:
        return "Missing required fields", 400

    # Adding the new student to the list
    studentlist.append({'ID': newid, 'NAME': newname, 'CATEGORY': newcategory, 'QUANTITY': newquantity, 'STATUS': newstatus})
    print("A new household item has been inserted")
    return "A new household item is added", 201

@app.route('/householditems/all', methods=['GET'])
def allhouseholditems():
    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)

    # Read operations on the database
    sql = "SELECT * FROM householditems" #is this supposed to be select from users instead?
    userrows = execute_read_query(mycon, sql)

    # Convert rows to a JSON-friendly format
    users = [{"ID": row[0], "NAME": row[1], "CATEGORY": row[2], "QUANTITY": row[3], "STATUS": row[4]} for user in userrows]
    return jsonify(users)
@app.route('/householditems/single', methods=['GET'])
def singleuser():
    # request.args consists of parameter arguments passed in request. 
    # Below code retriving parameter 'id' from request arguments 
    if 'ID' in request.args:    
        ID = int(request.args['ID'])
    else:
        return 'Error: No ID is provided!'
    
    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)
    sql = "select * from users"
    userrows = execute_read_query(mycon, sql)
    results = []

    for item in householditemslist:
        if item['ID']== ID:
            results.append(item)
    return jsonify(results)

@app.route('/householditems/insertnewitem', methods=['POST'])
def insertnewuser():
    userinput = request.get_json() # Pass new user info in JSON format within Body of the request
    newid = userinput['ID']
    newname = userinput['NAME']
    newcategory = userinput['CATEGORY']
    newquantity = userinput['QUANTITY']
    newstatus = userinput['STATUS']
    

    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)
    sql = "insert into users(newid, newname, newcategory, newquantity, newstatus) values ('%s','%s','%s','%s','%s')" % (newid, newname, newcategory, newquantity, newstatus)

    execute_update_query(mycon, sql)
    return 'Add user request successful!'

@app.route('/householditems/delete', methods=['DELETE'])
#how to delete by ID
#@app.route('/delete_householditems/<int:item_id>', methods=['DELETE'])
@app.route('/householditems/deleteuser', methods=['DELETE'])
def api_delete_user_byID():
    userinput = request.get_json() # Pass user ID in JSON format within Body of the request
    idtodelete = userinput['id']
    
    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)
    sql = "delete from users where id = %s" % (idtodelete)
    execute_update_query(mycon, sql)
        
    return "Delete request successful!"

# Update user information using request PUT method
@app.route('/users/updatehouseholditems', methods=['PUT'])
def updatehouseholditems():
    userinput = request.get_json() # Pass user ID and email in JSON format within Body of the request
    newid = userinput['ID']
    newname = userinput['NAME']


    mycreds = creds.myCreds()
    mycon = DBconnection(mycreds.hostname, mycreds.username, mycreds.password, mycreds.database)
    sql = "update users set name='%s' where id='%s'" % (newname, newid)

    execute_update_query(mycon, sql)
    return 'User update successful!'

DBconnection("cis2368database.cqznz0sza3gn.us-east-1.rds.amazonaws.com","admin","password","cis2368database")
#try changing database name to cis2368db1
app.run()
#print DBconnection 


