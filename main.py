from fastapi import FastAPI
from routes.crud import user
from routes.login import userlogin
from routes.fileupload import file
from routes.preprocess import pre
import os
# from decouple import config

# os.environ["MONGODB_URI"] = config("MONGODB_URI")
# os.environ["SECRET_KEY"] = config("SECRET_KEY")


app = FastAPI()
app.include_router(user)
app.include_router(userlogin)
app.include_router(file)
app.include_router(pre)

@app.get("/")
async def home():
    return {"message": "Hello World"}