from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class PlaylistCreate(BaseModel):
    name:str
    description:Optional[str]=None
    genre:Optional[str]=None

class playlistSongAdd(BaseModel):
    song_id:int



class PlaylistResponse(BaseModel):
    playlist_id:int
    user_id:int
    name:str
    description:Optional[str]
    genre:Optional[str]
    songs:List[int]

    class Config:
        from_attributes=True
