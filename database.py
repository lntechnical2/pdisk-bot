import pymongo 
import os

DB_NAME = os.environ.get("DB_NAME","")
DB_URL = os.environ.get("DB_URL","")
mongo = pymongo.MongoClient(DB_URL)
db = mongo[DB_NAME]
dbcol = db["USER"]

def insert(chat_id):
            user_id = int(chat_id)
            user_det = {"_id":user_id,"api_key":None}
            try:
            	dbcol.insert_one(user_det)
            except:
            	pass

def find(chat_id):
	user_id = chat_id
	data = dbcol.find_one({"_id":user_id})
	api_key = data["api_key"]
	return api_key

def set(chat_id,api_key):
	 dbcol.update_one({"_id":chat_id},{"$set":{"api_key":api_key}})

def getid():
    values = []
    for key  in dbcol.find():
         id = key["_id"]
         values.append(id) 
    return values
