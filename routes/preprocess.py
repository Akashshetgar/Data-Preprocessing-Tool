from fastapi import FastAPI, Query,Body
from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
import pandas as pd
from typing import List
from config.db import db,users
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

pre = APIRouter()

collection = db["datasets"]

@pre.get("/get_csv_column_info/{user_id}")
async def get_csv_column_info(user_id: str):
    result = collection.find_one({"id": user_id})
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    dict_file = result["file"]
    df = pd.DataFrame.from_dict(dict_file)
    
    # Load CSV data into a Pandas DataFrame
    # df = pd.read_csv(csv_file)
    
    # Get column names and data types
    column_info = [{"column_name": col, "data_type": str(df[col].dtype)} for col in df.columns]
    
    return column_info

@pre.get("/rename_colums/{user_id}/{old_name}/{new_name}")
async def rename_columns(user_id:str, old_name:str, new_name:str):
    global collection
    result = collection.find_one({"id": user_id})
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    dict_file = result["file"]
    df = pd.DataFrame.from_dict(dict_file)

    try:
        df.rename(columns={old_name: new_name}, inplace=True)
        data = df.to_dict(orient='records')
        obj= {
                "id":user_id, 
                "file":data
            }
        #deleting the previous data
        if db["datasets"].find_one({"id":user_id}): 
            db["datasets"].delete_one({"id":user_id})
        collection = db["datasets"]
        collection.insert_one(obj)
        return {"message": "Column renamed successfully"}
    except Exception as e:
        return {"message": "Column not found", "error": str(e)}

@pre.get("/drop_columns/{user_id}/{column_name}")
async def drop_columns(user_id:str, column_name:str):
    global collection
    result = collection.find_one({"id": user_id})
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    dict_file = result["file"]
    df = pd.DataFrame.from_dict(dict_file)

    try:
        df.drop(columns=column_name, inplace=True)
        data = df.to_dict(orient='records')
        obj= {
                "id":user_id, 
                "file":data
            }
        #deleting the previous data
        if db["datasets"].find_one({"id":user_id}): 
            db["datasets"].delete_one({"id":user_id})
        collection = db["datasets"]
        collection.insert_one(obj)
        return {"message": "Column dropped successfully"}
    except Exception as e:
        return {"message": "Column not found", "error": str(e)}
    
@pre.get("/fill_nan/{user_id}/{column_name}/{isvalue}/{value}")
async def fill_nan(user_id:str, column_name:str, isvalue:str, value:str):
    global collection
    result = collection.find_one({"id": user_id})
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    dict_file = result["file"]
    df = pd.DataFrame.from_dict(dict_file)

    try:
        if isvalue == "true":
            df[column_name].fillna(value, inplace=True)
        else:
            df[column_name].fillna(method = value, inplace=True)
        data = df.to_dict(orient='records')
        obj= {
                "id":user_id, 
                "file":data
            }
        #deleting the previous data
        if db["datasets"].find_one({"id":user_id}): 
            db["datasets"].delete_one({"id":user_id})
        collection = db["datasets"]
        collection.insert_one(obj)
        return {"message": "NaN values filled successfully"}
    except Exception as e:
        return {"message": "Column not found", "error": str(e)}
    
@pre.get("/drop_nan/{user_id}/{column_name}")
async def drop_nan(user_id:str, column_name:str):
    global collection
    result = collection.find_one({"id": user_id})
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    dict_file = result["file"]
    df = pd.DataFrame.from_dict(dict_file)

    try:
        df.dropna(subset=[column_name], inplace=True)
        data = df.to_dict(orient='records')
        obj= {
                "id":user_id, 
                "file":data
            }
        #deleting the previous data
        if db["datasets"].find_one({"id":user_id}): 
            db["datasets"].delete_one({"id":user_id})
        collection = db["datasets"]
        collection.insert_one(obj)
        return {"message": "NaN values dropped successfully"}
    except Exception as e:
        return {"message": "Column not found", "error": str(e)}
    

@pre.get("/one-hot-encoding/{user_id}/{column_names}")
async def one_hot_encoding(user_id:str, column_names: str):
    global collection
    result = collection.find_one({"id": user_id})
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    dict_file = result["file"]
    df = pd.DataFrame.from_dict(dict_file)
    columns = column_names.split(",")
    
  

    try:

        try:
            df = pd.get_dummies(df, columns=columns)
        except Exception as e:
            return {"message": "error", "error": str(e)}
        
        # df = pd.concat([df, encoded_data], axis=1)
        data = df.to_dict(orient='records')
        obj= {
                "id":user_id, 
                "file":data
            }
        #deleting the previous data
        if db["datasets"].find_one({"id":user_id}): 
            db["datasets"].delete_one({"id":user_id})
        collection = db["datasets"]
        collection.insert_one(obj)
        return {"message":"One hot encoding completed successfully for columns: {}".format(columns)}
    except Exception as e:
        return {"message": "Column not found", "error": str(e)}
    
@pre.get('/tokenize/{user_id}/{column_name}')
async def tokenize(user_id:str, column_name:str):
    global collection
    result = collection.find_one({"id": user_id})
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    dict_file = result["file"]
    df = pd.DataFrame.from_dict(dict_file)

    try:
        tokenized_col = df[column_name].apply(lambda x: word_tokenize(x) if type(x) == str else x)
        new_col_name = f"{column_name}_tokenized"
        df[new_col_name] = tokenized_col
        data = df.to_dict(orient='records')
        obj= {
                "id":user_id, 
                "file":data
            }
        #deleting the previous data
        if db["datasets"].find_one({"id":user_id}): 
            db["datasets"].delete_one({"id":user_id})
        collection = db["datasets"]
        collection.insert_one(obj)
        return {"message": "Tokenization done successfully"}
    except Exception as e:
        return {"message": "Column not found", "error": str(e)}
    
@pre.get('/remove_stopwords/{user_id}/{column_name}')
async def remove_stopwords(user_id:str, column_name:str):
    global collection
    result = collection.find_one({"id": user_id})
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    dict_file = result["file"]
    df = pd.DataFrame.from_dict(dict_file)

    try:
        new_col_name = f"{column_name}_stopwords_removed"
        stop_words = set(stopwords.words('english'))
        df[new_col_name] = df[column_name].apply(lambda x: [word for word in x if word not in stop_words])
        data = df.to_dict(orient='records')
        obj= {
                "id":user_id, 
                "file":data
            }
        #deleting the previous data
        if db["datasets"].find_one({"id":user_id}): 
            db["datasets"].delete_one({"id":user_id})
        collection = db["datasets"]
        collection.insert_one(obj)
        return {"message": "Stopwords removed successfully"}
    except Exception as e:
        return {"message": "Column not found", "error": str(e)}



