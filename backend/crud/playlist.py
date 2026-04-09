from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.models.playlist import Playlist
from backend.schemas.playlist import PlaylistCreate
from fastapi import HTTPException

class PlaylistCrud:
    @staticmethod
    async def new_playlist_theme(db:AsyncSession,playlist:PlaylistCreate,user_id:int)->Playlist|None:
        new_ply=Playlist(name=playlist.name,description=playlist.description, genre=playlist.genre,user_id=user_id)
        db.add(new_ply)
        await db.flush()
        return new_ply
    
    @staticmethod
    async def get_all(db: AsyncSession) -> list[Playlist]:
        result = await db.execute(select(Playlist))
        return result.scalars().all()


    @staticmethod
    async def get_by_id(db:AsyncSession,playlist_id:int)->Playlist|None:
        ply = await db.get(Playlist,playlist_id)
        if ply:
            return ply
        return None
    
    @staticmethod
    async def delete_by_id(db: AsyncSession, playlist_id: int) -> dict:  # user_id 제거
        del_ply = await db.get(Playlist, playlist_id)
        
        if not del_ply:
            raise HTTPException(status_code=404, detail="플레이리스트가 없습니다")
        
        await db.delete(del_ply)
        await db.flush()
        return {"msg": "플리가 삭제됨"}
    
