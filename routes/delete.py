from fastapi import FastAPI, File, UploadFile, Depends
from fastapi import APIRouter
from models.pipelineModel import PipelineModel
from bson import ObjectId
import pandas as pd
from config.db import db,users
import json
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

rem = APIRouter()

@rem.delete("/delete_dataset/{user_id}")
async def delete_dataset(user_id: str= Depends(oauth2_scheme)):
    # Delete the user with the given user_id
    result = db['datasets'].delete_one({"id": user_id})
    
    if result.deleted_count == 1:
        return {"message": f"User with user_id {user_id} has been deleted."}
    else:
        return {"message": f"User with user_id {user_id} was not found."}