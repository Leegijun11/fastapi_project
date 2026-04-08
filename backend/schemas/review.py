from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ReviewCreate(BaseModel):
    rating: int=Field(ge=1,le=5)
    comment:str

class ReviewUpdate(BaseModel):
    rating:Optional[int]=Field(default=None,ge=1,le=5)
    comment:Optional[str]=None

class ReviewResponse(BaseModel):
    review_id: int
    song_id: int
    user_id: int
    rating: int
    comment: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
