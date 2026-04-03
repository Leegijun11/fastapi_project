from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ReviewCreate(BaseModel):
    rating: int=Field(ge=1,le=5)
    comment:str

class ReviewUpdate(BaseModel):
    rating:Optional[int]=Field(default=None,ge=1,le=5)
    comment:Optional[str]=None


    