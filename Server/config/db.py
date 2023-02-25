from pymongo import MongoClient
import os
db_connection = MongoClient(os.environ['MONGODB_URI'])
db = db_connection.dataforge
users = db["users"]