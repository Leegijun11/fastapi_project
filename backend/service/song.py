from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from backend.models.song import Song
from backend.schemas.song import SongCreate, SongRead, SongUpdate
from backend.crud.song import SongCrud
from backend.auth import get_user_id
class SongService:
    @staticmethod
    async def createSong(db:AsyncSession,song:SongCreate,current_user_id: int):
        if not current_user_id:
            raise HTTPException(status_code=401, detail="로그인이 필요한 서비스입니다.")
        try:
            new_song=await SongCrud.new_song(current_user_id,song,db)
            await db.commit()
            await db.refresh(new_song)
            return new_song
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=500, detail="서버 오류로 인한 생성 실패")
        
    @staticmethod #User
    async def song_all(db:AsyncSession,current_user_id: int):
        if not current_user_id:
            raise HTTPException(status_code=401, detail="로그인이 필요한 서비스입니다.")
        db_song_all= await SongCrud.get_all(db)
        if not db_song_all:
            raise HTTPException(status_code=404, detail="전체 노래 조회 실패")
        return db_song_all
    
    @staticmethod #User
    async def song_detail(db:AsyncSession,song_id:int,current_user_id: int)->Song|None:
        if not current_user_id:
            raise HTTPException(status_code=401, detail="로그인이 필요한 서비스입니다.")
        db_song_detail= await SongCrud.get_by_id(db,song_id)
        if not db_song_detail:
            raise HTTPException(status_code=404, detail="노래 조회 실패")
        return db_song_detail
    
    @staticmethod
    async def update_song(db: AsyncSession, song_id: int, song: SongUpdate, current_user_id: int):
        # 1. 해당 노래 존재 여부 및 데이터 조회
        db_song = await SongCrud.get_by_id(db, song_id)
        if not db_song:
            raise HTTPException(status_code=404, detail="해당 노래가 존재하지 않습니다.")

        # 2. [Owner 체크]  get_owner의 로직을 직접 적용
        if db_song.user_id != current_user_id:
            raise HTTPException(status_code=403, detail="본인의 노래만 수정할 수 있습니다.")

        # 3. 업데이트 수행
        db_update_song = await SongCrud.update_by_id(db, song_id, song) # CRUD 인자 순서 통일(db 먼저)
        await db.commit()
        await db.refresh(db_update_song)
        return db_update_song

    @staticmethod
    async def delete_song(db: AsyncSession, song_id: int, current_user_id: int):
        # 1. 해당 노래 존재 여부 확인을 위한 조회
        db_song = await SongCrud.get_by_id(db, song_id)
        if not db_song:
            raise HTTPException(status_code=404, detail="노래가 없습니다.")

        # 2. [Owner 체크]
       
        if db_song.user_id != current_user_id:
             raise HTTPException(status_code=403, detail="삭제 권한이 없습니다.")

        # 3. 삭제 진행
        await SongCrud.delete_by_id(db, song_id) # CRUD 인자 순서 통일
        await db.commit()
        
        return {"msg": "삭제 성공", "song_id": song_id}