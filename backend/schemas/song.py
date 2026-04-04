from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SongCreate(BaseModel):
    title:str
    artist:str
    genre:str


class SongRead(BaseModel):
    song_id:int
    title:str
    artist:str
    genre:str
    created_at:datetime

    class Config:
        from_attributes=True

class SongList(BaseModel):
    songs: List[SongRead]

class SongUpdate(BaseModel):
    title:Optional[str]=None
    artist:Optional[str]=None
    genre:Optional[str]=None

class DeleteMessage(BaseModel):
    message:str

