from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas.playlistsong import PlaylistSongCreate,PlaylistSongRead
from backend.database import get_db
from backend.service.playlistsong import PlaylistsongService

router=APIRouter(prefix="/playlist",tags=["Playlist"])

@router.post("/{playlist_id}/songs")
async def new_song(playlistsong:PlaylistSongCreate,playlist_id:int,response:Response,db:AsyncSession=Depends(get_db)):
    new_song_at_ply = await PlaylistsongService.new_song(db,playlist_id,playlistsong.song_id)
    return new_song_at_ply


@router.delete("/{playlist_id}/songs/{songs_id}")
async def del_song(playlist_id:int,songs_id:int,response:Response,db:AsyncSession=Depends(get_db)):
    del_song = await PlaylistsongService.del_song(db,playlist_id,songs_id)
    return {"msg": "노래가 삭제됨"}