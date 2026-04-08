from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from backend.models.playlistsong import PlaylistSong
from backend.schemas.playlistsong import PlaylistSongCreate, PlaylistSongRead
from backend.crud.playlistsong import PlaylistsongCrud

class PlaylistsongService:

    @staticmethod
    async def new_song(db:AsyncSession,playlist_id:int,song_id:int):
        try:
            song_data = PlaylistSongCreate(song_id=song_id)

            new_entry = await PlaylistsongCrud.new_song_at_ply(db,playlist_id,song_data)
            await db.commit()
            await db.refresh(new_entry)
            return new_entry
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=500, detail="서버 오류로 인한 생성 실패")
        
    @staticmethod
    async def del_song(db:AsyncSession,playlist_id:int,song_id:int):
        db_del_song = await PlaylistsongCrud.delete_song_at_ply(db, playlist_id,song_id)
        if not db_del_song:
            raise HTTPException(status_code=404, detail="다시 시도해주세요")
        await db.commit()
        return db_del_song