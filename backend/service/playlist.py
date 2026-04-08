from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from backend.models.playlist import Playlist
from backend.schemas.playlist import PlaylistCreate, PlaylistResponse
from backend.crud.playlist import PlaylistCrud

class PlaylistService:

    @staticmethod
    async def new_theme(db:AsyncSession,user_id:int, playlist:PlaylistCreate,current_user_id: int):
        if not current_user_id:
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
        # 1. 삭제 전 해당 플레이리스트가 존재하는지, 주인은 누구인지 조회
        db_ply = await PlaylistCrud.get_by_id(db, playlist_id)
        if not db_ply:
            raise HTTPException(status_code=404, detail="플레이리스트를 찾을 수 없습니다.")

        # 2. [Owner 체크] 작성자 ID와 현재 로그인 ID 비교
        if db_ply.user_id != current_user_id:
            raise HTTPException(status_code=403, detail="본인의 플레이리스트만 삭제할 수 있습니다.")

        # 3. 삭제 수행
        result = await PlaylistCrud.delete_by_id(db, playlist_id)
        if not result:
            raise HTTPException(status_code=404, detail="삭제 실패")
            
        await db.commit()
        return {"message": "플레이리스트가 성공적으로 삭제되었습니다."}