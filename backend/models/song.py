from backend.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import String, TIMESTAMP, func
from typing import Optional, List, TYPE_CHECKING


if TYPE_CHECKING:
    from .playlist import Playlist

class Song(Base):
    __tablename__ = "songs"

    song_id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    genre: Mapped[str] = mapped_column(String(255), nullable=False)
    artist: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=True)

    playlists: Mapped[List["Playlist"]] = relationship(
        secondary="playlist_songs",
        back_populates="songs"
    )
