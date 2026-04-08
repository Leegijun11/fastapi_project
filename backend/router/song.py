from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas.song import SongRead, SongCreate, SongUpdate
from backend.database import get_db
from backend.service.song import SongService

router=APIRouter(prefix="/songs",tags=["Song API"])


@router.post("/",response_model=SongRead)
async def create_song(song:SongCreate, db:AsyncSession=Depends(get_db)):
    return await SongService.createSong(db, song)

@router.get("/",response_model=list[SongRead])
async def get_songs(db:AsyncSession=Depends(get_db)):
    return await SongService.song_all(db)

@router.put("/{song_id}")
async def update_song(
    song_id:int,
    song:SongUpdate,
    db:AsyncSession=Depends(get_db),
):
    return await SongService.update_song(db, song_id, song)

@router.delete("/{song_id}")
async def delete_song(song_id:int, db:AsyncSession=Depends(get_db)):
    return await SongService.delete_song(db, song_id)