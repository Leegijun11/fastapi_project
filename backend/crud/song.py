from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.models.song import Song
from backend.schemas.song import SongCreate,SongUpdate

class SongCrud:
    @staticmethod
    async def get_by_id(db:AsyncSession,song_id:int)->Song|None:
        result=await db.execute(select(Song).filter(Song.song_id == song_id))
        return result.scalar_one_or_none()        

    @staticmethod
    async def get_all(db: AsyncSession) -> list[Song]:
        result = await db.execute(select(Song))
        return result.scalars().all()
        
    @staticmethod
    async def new_song(db:AsyncSession,song:SongCreate)->Song|None:
        new_song = Song(title=song.title, artist=song.artist, genre=song.genre)
        db.add(new_song)
        await db.flush()
        return new_song
    
    @staticmethod
    async def update_by_id(song_id:int,song:SongUpdate,db:AsyncSession)->Song|None:
        update_song = await db.execute(select(Song).filter(Song.song_id == song_id))
        updating_song = update_song.scalars().first()
        if updating_song :
            updating_song.title = song.title
            updating_song.artist= song.artist
            updating_song.genre = song.genre
            await db.flush()
            return {"title": updating_song.title,
                    "artist":updating_song.artist,
                    "genre": updating_song.genre
                    }
        return None
    
    @staticmethod
    async def delete_by_id(song_id:int,db:AsyncSession)->Song|None:
        del_song=await db.get(Song, song_id)
        if del_song:
            await db.delete(del_song)
            await db.flush()
            return {"msg": "음악이 삭제됨"}
        return None
    