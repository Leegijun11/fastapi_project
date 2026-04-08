from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from backend.models.song import Song
from backend.schemas.song import SongCreate, SongRead, SongUpdate
from backend.crud.song import SongCrud

class SongService:
    @staticmethod
    async def createSong(db:AsyncSession,song:SongCreate):
        try:
            new_song=await SongCrud.new_song(db,song)
            await db.commit()
            await db.refresh(new_song)
            return new_song
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=500, detail="서버 오류로 인한 생성 실패")
        
    @staticmethod
    async def song_all(db:AsyncSession):
        db_song_all= await SongCrud.get_all(db)
        if not db_song_all:
            raise HTTPException(status_code=404, detail="전체 노래 조회 실패")
        return db_song_all
    
    @staticmethod
    async def song_detail(db:AsyncSession,song_id:int)->Song|None:
        db_song_detail= await SongCrud.get_by_id(db,song_id)
        if not db_song_detail:
            raise HTTPException(status_code=404, detail="노래 조회 실패")
        return db_song_detail
    
    @staticmethod
    async def update_song(db:AsyncSession, song_id:int, song: SongUpdate):
        db_update_song = await SongCrud.update_by_id(song_id, song, db)
        if not db_update_song:
            raise HTTPException(status_code=404, detail="해당 id를 가진 song이 존재하지 않습니다")
        await db.commit()
        return db_update_song
    
    @staticmethod
    async def delete_song(db:AsyncSession,song_id:int)->Song|None:
        db_del_song = await SongCrud.delete_by_id(song_id,db)
        if not db_del_song:
            raise HTTPException(status_code=404, detail="노래삭제 실패")
        await db.commit()
        return db_del_song
        