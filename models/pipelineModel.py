from pydantic import BaseModel, Field
from typing import List

class PipelineModel(BaseModel):
    pipeline_name:str
    pipeline: list[list[str]]