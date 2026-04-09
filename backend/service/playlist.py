from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from backend.models.playlist import Playlist
from backend.schemas.playlist import PlaylistCreate, PlaylistResponse
from backend.crud.playlist import PlaylistCrud

class PlaylistService:

    @staticmethod
    async def new_theme(db:AsyncSession,user_id:int, playlist:PlaylistCreate):
        if not user_id:
            raise HTTPException(status_code=401, detail="로그인이 필요한 서비스입니다.")
        try:
           new_ply_model=await PlaylistCrud.new_playlist_theme(db,playlist,user_id)
           await db.commit()
           await db.refresh(new_ply_model)
           return new_ply_model
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=500, detail="서버 오류로인한 생성 실패")
        
    @staticmethod
    async def all_ply(db:AsyncSession,current_user_id: int):
        if not current_user_id:
            raise HTTPException(status_code=401, detail="로그인이 필요한 서비스입니다.")
        db_all_ply=await PlaylistCrud.get_all(db)
        if not db_all_ply:
            raise HTTPException(status_code=404, detail="플레이 리스트를 찾을 수 없다")
        return db_all_ply
    
    @staticmethod
    async def my_ply(db:AsyncSession, playlist_id:int,current_user_id: int):
        if not current_user_id:
            raise HTTPException(status_code=401, detail="로그인이 필요한 서비스입니다.")
        db_ply=await PlaylistCrud.get_by_id(db,playlist_id)
        if not db_ply:
            raise HTTPException(status_code=404, detail="해당 Id를 가진 플레이 리스트를 찾을 수 없다")
        return db_ply
    
    @staticmethod
    async def del_ply(db: AsyncSession, playlist_id: int, current_user_id: int):
        db_ply = await PlaylistCrud.get_by_id(db, playlist_id)
        if not db_ply:
            raise HTTPException(status_code=404, detail="플레이리스트를 찾을 수 없습니다.")
        
        if db_ply.user_id != current_user_id:
            raise HTTPException(status_code=403, detail="삭제 권한이 없습니다.")
        
        result = await PlaylistCrud.delete_by_id(db, playlist_id)
        await db.commit()
        return result