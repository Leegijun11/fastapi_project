from pydantic import BaseModel
from typing import List

class PlaylistSongCreate(BaseModel):
    song_id:int

class PlaylistSongRead(BaseModel):
    id:int
    playlist_id:int
    song_id:int

    class Config:
        from_attributes=True


class PlaylistSongList(BaseModel):
    items:List[PlaylistSongRead]


class EditMessage(BaseModel):
    message:str

class DeleteMessage(BaseModel):
    message:str