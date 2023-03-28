from pydantic import BaseModel, Field
from fastapi import FastAPI, File, UploadFile
from typing import Optional
from bson.objectid import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class PipelineModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    pipeline_name:str
    pipeline: str