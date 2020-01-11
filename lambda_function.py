import json
import logging
import psycopg2
from datetime import datetime
#replace db_host for your rds cluster host
db_host = "xxxxxxxxxxxxxxxxxxxxxx"
db_port = 5432
db_name = "postgres"
db_user = "postgres"
db_pass = "postgres"
# inicializo logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Client():
    Name = str()
    Surname = str()
    Date = str()
    
    def __init__(self,Name,Surname,Date):
        self.Name = Name
        self.Surname = Surname
        self.Date = Date
    
    def setName (self,Name):
        self.Name = Name

    def setSurname (self,Surname):
        self.Surname = Surname

    def setDate (self,Date):
        self.Date = Date

    def getName (self):
        return self.Name

    def getSurname (self):
        return self.Surname

    def getDate (self):
        return self.Date


def InsertData(Client):
	RowsAffected=0
	try:
		conn = create_conn()
		cursor = conn.cursor()
		postgres_insert_query = 'INSERT INTO "public"."clients"  ("name","surname","DATE") VALUES ('+"'"+str(Client.getName())+"','"+str(Client.getSurname())+"','"+str(Client.getDate())+"')"
		cursor.execute(postgres_insert_query)
		conn.commit()
		RowsAffected = cursor.rowcount
	except Exception as e:
		logger.error(e)
		logger.error("Error ocurred while inserting")
	cursor.close()
	conn.close()
	return RowsAffected
   
def SelectData(Client):
	output = str()
	try:
		conn = create_conn()
		cursor = conn.cursor()
		query_cmd = 'select "name","surname","DATE" from "public"."clients" where "name"='+"'"+str(Client.getName())+"'"+' and "surname"='+"'"+str(Client.getSurname())+"'"
		output = fetch(conn, query_cmd)
	except Exception as e:
		logger.error(e)
		logger.error("Error ocurred while reading")
	
	cursor.close()
	conn.close()
	return str(output)
	
def create_conn():
    conn = None
    try:
        conn = psycopg2.connect("dbname={} user={} host={} password={}".format(db_name,db_user,db_host,db_pass))
    except:
        print("Cannot connect.")
    return conn

def fetch(conn, query):
	result = []
	cursor = conn.cursor()
	cursor.execute(query)
	raw = cursor.fetchall()
	for line in raw:
		result.append(line)
	return result


def lambda_handler(event, context):
	RowsAffected=0
	dateNow = datetime.now()
	event2 = json.loads(event['body'])
	client = Client (event2['clientName'],event2['clientSurname'],dateNow)
	logger.info (event2['clientName'])
	logger.info (event2['clientSurname'])
	op = event2['operation']
	if op == 'insert':
		output = InsertData(client)
		responseBody = '{"message": "'+str(output)+'"}'
		logger.info(str(responseBody))
	elif op == 'select':
		output = SelectData(client)    
		responseBody = '{"message": "'+str(output)+'"}'
		logger.info(str(responseBody))
	else:
		responseBody = '{"message": "You must send operation (insert/select) and clientName/clientSurname tags on body }'
		logger.info(str(responseBody))
	
	responseObject = {}
	responseObject['statusCode'] = 200
	responseObject['headers'] = {}
	responseObject['headers']['Content-Type'] = 'application/json'
	responseObject['body'] = json.dumps(responseBody)
	return responseObject