from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas.playlistsong import PlaylistSongCreate,PlaylistSongRead
from backend.database import get_db
from backend.service.playlistsong import PlaylistsongService
from backend.auth import get_current_user
router=APIRouter(prefix="/playlist",tags=["Playlist"])

@router.post("/{playlist_id}/songs") # o
async def new_song(playlistsong:PlaylistSongCreate,playlist_id:int,response:Response,db:AsyncSession=Depends(get_db),
                   current_user= Depends(get_current_user)):
    new_song_at_ply = await PlaylistsongService.new_song(db,playlist_id,playlistsong.song_id, current_user.user_id)
    return new_song_at_ply


@router.delete("/{playlist_id}/songs/{songs_id}") # o
async def del_song(playlist_id:int,songs_id:int,response:Response,db:AsyncSession=Depends(get_db),
                current_user= Depends(get_current_user)   ):
    del_song = await PlaylistsongService.del_song(db,playlist_id,songs_id, current_user.user_id)
    return {"msg": "노래가 삭제됨"}

@router.get("/playlist/{playlist_id}/songs") #u
async def get_songs_in_playlist(
    playlist_id: int,
    db: AsyncSession = Depends(get_db),
    current_user= Depends(get_current_user)
):
    return await PlaylistsongService.get_playlist_with_songs(db, playlist_id, current_user.user_id)