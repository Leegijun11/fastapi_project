from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from models.song import Song
from schemas.song import SongCreate, SongUpdate, SongList, SongRead
# from crud

# class SongService:

#     @staticmethod
#     async def create_song(db: AsyncSession, song_data: SongCreate) -> Song:
#     # 곡 등록 
#     # 1. 중복검사 2.데이터 정규화(공백제거) 3.DB 저장 4.트랜잭션 관리
#     existing_song = await SongCrud.get_by_title_and_artist(db,
#                                                            title=song_data.title.strip()
#                                                            artist=song_data.artist.strip()
#                                                            )
#     if existing_song:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f"'{song_data.artist}의 '{song_data.title}은(는) 이미 등록된 곡입니다"
#         )
#     song_data.genre = song_data.genre.strip()

#     try:
#         new_song = await SongCrud.create(db, song_data)
#         await db.commit()
#         await db.refresh(new_song)
#         return new_song
#     except Exception as e:
#         await db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="서버 내부 오류로 곡을 등록할 수 없습니다."
#         )
    
  
#     @staticmethod
#     async def get_all_songs(db: AsyncSession, genre: str = None) -> SongList:
#     # 곡 목록 조회(장르 필터링)
#     if genre:          # 장르가 들어왔으면 그 장르를 가진 노래만 조회하는 함수
#         songs = await SongCrud.get_by_genre(db, genre)
#     else:              # 장르가 들어와있지 않으면 전체 노래 
#         songs = await SongCrud.get_all(db) 
#     return SongList(songs=songs)
#     # Crud 작성해주시면 그거에 맞춰서 함수명이나 비즈니스 로직 자체 바꿀게요!    