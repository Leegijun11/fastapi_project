from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

class PlaylistSong(Base):
    __tablename__ = "playlist_songs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    playlist_id: Mapped[int] = mapped_column(ForeignKey("playlists.playlist_id"), nullable=False)
    song_id: Mapped[int] = mapped_column(ForeignKey("songs.song_id"), nullable=False)

