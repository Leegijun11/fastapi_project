from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from backend.models.playlistsong import PlaylistSong
from backend.models.song import Song
from backend.schemas.playlistsong import PlaylistSongCreate, PlaylistSongRead
from backend.crud.playlistsong import PlaylistsongCrud
from sqlalchemy import select
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
    
    @staticmethod
    async def get_song_ids(db, playlist_id: int) -> list[int]:

        result = await db.execute(
            select(PlaylistSong.song_id).where(PlaylistSong.playlist_id == playlist_id)
        )
        return result.scalars().all()
    

    @staticmethod
    async def get_playlist_with_songs(db, playlist_id: int):
        # 1. PlaylistSong에서 해당 playlist_id의 레코드 조회
        result = await db.execute(
            select(PlaylistSong).where(PlaylistSong.playlist_id == playlist_id)
        )
        playlist_songs = result.scalars().all()

        if not playlist_songs:
            raise HTTPException(status_code=404, detail="플레이리스트가 없습니다")

        # 2. song_id 리스트 추출
        song_ids = [ps.song_id for ps in playlist_songs]

        # 3. Song 테이블에서 대응되는 곡 조회
        result = await db.execute(
            select(Song).where(Song.song_id.in_(song_ids))
        )
        songs = result.scalars().all()

        song_titles = [song.title for song in songs]

        return {"playlist_id": playlist_id, "songs": song_titles}