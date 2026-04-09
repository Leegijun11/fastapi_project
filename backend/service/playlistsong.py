from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from backend.models.playlistsong import PlaylistSong
from backend.models.song import Song
from backend.schemas.playlistsong import PlaylistSongCreate, PlaylistSongRead
from backend.crud.playlistsong import PlaylistsongCrud
from backend.crud.playlist import PlaylistCrud
from sqlalchemy import select
class PlaylistsongService:

    @staticmethod # o
    async def new_song(db:AsyncSession,playlist_id:int,song_id:int, current_user_id: int):
        playlist = await PlaylistCrud.get_by_id(db,playlist_id)
        if not playlist:
            raise HTTPException(status_code=404, detail="플레이리스트를 찾을 수 없습니다.")
        if playlist.user_id != current_user_id:
            raise HTTPException(status_code=403, detail="본인의 플레이리스트에서만 노래를 추가할 수 있습니다.")
        try:
            song_data = PlaylistSongCreate(song_id=song_id)
            new_entry = await PlaylistsongCrud.new_song_at_ply(db,playlist_id,song_data)
            await db.commit()
            await db.refresh(new_entry)
            return new_entry
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=500, detail="서버 오류로 인한 생성 실패")
        
    @staticmethod # o
    async def del_song(db:AsyncSession,playlist_id:int,song_id:int, current_user_id: int):
        playlist = await PlaylistCrud.get_by_id(db, playlist_id)    
        if not playlist:
            raise HTTPException(status_code=404, detail="플레이리스트를 찾을 수 없습니다.")
    # 2. [권한 체크] 플레이리스트 주인이 현재 로그인한 유저인지 확인
        if playlist.user_id != current_user_id:
          raise HTTPException(status_code=403, detail="본인의 플레이리스트에서만 노래를 삭제할 수 있습니다.")
        
        db_del_song = await PlaylistsongCrud.delete_song_at_ply(db, playlist_id, song_id)

        if not db_del_song:
            raise HTTPException(status_code=404, detail="다시 시도해주세요")

        await db.commit()
        return db_del_song
    
    
    @staticmethod #u
    async def get_playlist_with_songs(db, playlist_id: int,current_user_id:int):  
        if not current_user_id:
            raise HTTPException(status_code=401, detail="로그인이 필요한 서비스입니다.")
        result = await db.execute(
            select(PlaylistSong).where(PlaylistSong.playlist_id == playlist_id)
        )
        playlist_songs = result.scalars().all()
        if not playlist_songs:
            raise HTTPException(status_code=404, detail="플레이리스트가 없습니다")
        song_ids = [ps.song_id for ps in playlist_songs]     
        result = await db.execute(
            select(Song).where(Song.song_id.in_(song_ids))
        )
        songs = result.scalars().all()
        song_titles = [song.title for song in songs]
        return {"playlist_id": playlist_id, "songs": song_titles}