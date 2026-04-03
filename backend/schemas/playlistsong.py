from pydantic import BaseModel
from typing import List
from datetime import datetime

class PlaylistSongCreate(BaseModel):
    song_id:int

class PlaylistSongRead(BaseModel):
    song_id:int
    title:str
    artist:str
    genre:str
    created_at:datetime

    class Config:
        from_attributes=True




