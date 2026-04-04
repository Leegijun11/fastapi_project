from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.playlistsong import Playlistsong
from schemas.playlistsong import PlaylistSongCreate



class PlaylistsongCrud:
    @staticmethod
    async def new_song_at_ply(db:AsyncSession,playlist_id:int,newsong:PlaylistSongCreate)->Playlistsong|None:
        new_song = Playlistsong(playlist_id=playlist_id,song_id=newsong.song_id)
        db.add(new_song)
        await db.flush()
        return new_song
    
    async def delete_song_at_ply(db: AsyncSession, playlist_id: int, song_id: int) -> dict | None:
        result = await db.execute(
            select(Playlistsong).filter(
                Playlistsong.playlist_id == playlist_id,
                Playlistsong.song_id == song_id
            )
        )
        del_song = result.scalars().first()
        if del_song:
            await db.delete(del_song)
            await db.flush()
            return {"msg": "플리 안 노래가 삭제됨"}
        return None