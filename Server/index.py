from fastapi import FastAPI
from routes.crud import user
from routes.login import userlogin
from routes.fileupload import file
from routes.preprocess import pre
import os

os.environ['MONGODB_URI'] = "mongodb+srv://akashshetgar:NECHQPZa4yyMzmtZ@dataforgecluster1.v5fwvnn.mongodb.net/test"
os.environ['SECRET_KEY'] = "thisisasecretkey"

app = FastAPI()
app.include_router(user)
app.include_router(userlogin)
app.include_router(file)
app.include_router(pre)

@app.get("/")
async def home():
    return {"message": "Hello World"}