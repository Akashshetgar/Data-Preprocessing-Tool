from fastapi import FastAPI, File, UploadFile
from fastapi import APIRouter
from models.fileModel import FileModel
from bson import ObjectId
import pandas as pd
from config.db import db,users

file = APIRouter()



@file.post("/upload-csv/{user_id}")
async def upload_csv(user_id, file: UploadFile = File(...)):
    # Verify the user exists in the database
    user = users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return {"message": "User not found"}

    # Read the CSV file using pandas
    df = pd.read_csv(file.file,encoding='ISO-8859-1')


    #deleting the previous data
    if db["datasets"].find_one({"id":user_id}): 
        db["datasets"].delete_one({"id":user_id})

    # Save the data to MongoDB
    data = df.to_dict(orient='records')
    obj= {
            "id":user_id, 
            "file":data
        }
    collection = db["datasets"]
    collection.insert_one(obj)

    return {"message": f"{len(data)} records saved to datasets collection"}
