from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas.song import SongRead, SongCreate, SongUpdate
from backend.database import get_db
from backend.service.song import SongService
from backend.auth import get_current_user,get_owner
router=APIRouter(prefix="/songs",tags=["Song API"])


@router.post("/",response_model=SongRead)
async def create_song(song:SongCreate, db:AsyncSession=Depends(get_db),
                    current_user= Depends(get_current_user)):
    return await SongService.createSong(db, song, current_user.user_id)

@router.get("/",response_model=list[SongRead])
async def get_songs(db:AsyncSession=Depends(get_db),
                    current_user= Depends(get_current_user)):
    return await SongService.song_all(db, current_user.user_id)

@router.put("/{song_id}", response_model=SongRead)
async def update_song(
    song_id: int,
    song: SongUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user) # 로그인 확인 추가
):
    # 서비스에 current_user.user_id를 넘겨서 Owner 체크를 하게 합니다.
    return await SongService.update_song(db, song_id, song, current_user.user_id)

@router.delete("/{song_id}")
async def delete_song(
    song_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user) # 로그인 확인 추가
):
    # 서비스에 current_user.user_id를 넘겨서 Owner 체크를 하게 합니다.
    return await SongService.delete_song(db, song_id, current_user.user_id)