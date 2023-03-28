from fastapi import FastAPI, File, UploadFile
from fastapi import APIRouter
from models.fileModel import FileModel
from bson import ObjectId
import pandas as pd
from config.db import db,users
import json

pipe = APIRouter()

@pipe.post("/upload-pipeline/{user_id}/{pipeline_name}")
async def upload_csv(user_id, pipeline_name:str, pipeline:dict):
    # Verify the user exists in the database
    user = users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return {"message": "User not found"}

    # Read the CSV file using pandas
    try:
        # data = df.to_dict(orient='records')
        obj= {
                "id":user_id, 
                "pipeline":pipeline
            }
        collection = db["datasets"]
        collection.insert_one(obj)    
        
    except Exception as e:
         return {"message": "Error saving pipeline", "error": str(e)}

    return {"message": "Pipeline saved", "data": obj}