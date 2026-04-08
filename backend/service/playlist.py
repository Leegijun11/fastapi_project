from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from backend.models.playlist import Playlist
from backend.schemas.playlist import PlaylistCreate, PlaylistResponse
from backend.crud.playlist import PlaylistCrud

class PlaylistService:

    @staticmethod
    async def new_theme(db:AsyncSession,user_id:int, playlist:PlaylistCreate):
      
        try:
           new_ply_model=await PlaylistCrud.new_playlist_theme(db,playlist,user_id)
           await db.commit()
           await db.refresh(new_ply_model)
           return new_ply_model
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=500, detail="서버 오류로인한 생성 실패")
        
    @staticmethod
    async def all_ply(db:AsyncSession):
        db_all_ply=await PlaylistCrud.get_all(db)
        if not db_all_ply:
            raise HTTPException(status_code=404, detail="플레이 리스트를 찾을 수 없다")
        return db_all_ply
    
    @staticmethod
    async def my_ply(db:AsyncSession, playlist_id:int):
        db_ply=await PlaylistCrud.get_by_id(db,playlist_id)
        if not db_ply:
            raise HTTPException(status_code=404, detail="해당 Id를 가진 플레이 리스트를 찾을 수 없다")
        return db_ply
    
    @staticmethod
    async def del_ply(db:AsyncSession, playlist_id:int):
        db_del_ply = await PlaylistCrud.delete_by_id(db,playlist_id)
        if not db_del_ply:
            raise HTTPException(status_code=404, detail="플레이리스트 삭제 실패. 다시 시도해주세요")
        await db.commit()
        return db_del_ply