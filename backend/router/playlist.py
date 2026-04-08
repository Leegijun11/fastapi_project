from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas.playlist import PlaylistCreate,PlaylistResponse
from backend.database import get_db
from backend.service.playlist import PlaylistService
from backend.auth import get_current_user

router = APIRouter(prefix="/playlists", tags=["Playlists"])

@router.post("/{user_id}")
async def new_theme(user_id: int, playlist: PlaylistCreate, response: Response, db: AsyncSession = Depends(get_db),
                    current_user= Depends(get_current_user)):
    db_playlist = await PlaylistService.new_theme(db, user_id, playlist, current_user.user_id)
    return {"플레이리스트 ID",db_playlist.playlist_id}

@router.get("/") 
async def all_ply(response: Response, db: AsyncSession = Depends(get_db),
                  current_user= Depends(get_current_user)):
    db_all_ply = await PlaylistService.all_ply(db, current_user.user_id)
    return db_all_ply

@router.get("/{playlist_id}")
async def my_ply(playlist_id: int, response: Response, db: AsyncSession = Depends(get_db),
                 current_user= Depends(get_current_user)):
    db_my_ply = await PlaylistService.my_ply(db,playlist_id, current_user.user_id)
    return db_my_ply

@router.delete("/{playlist_id}")
async def del_ply(playlist_id: int, db: AsyncSession = Depends(get_db),
                  current_user = Depends(get_current_user)):
    await PlaylistService.del_ply(db,playlist_id,current_user.user_id)
    return {"message": "플레이리스트가 삭제되었습니다."} 
