from backend.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import String, TIMESTAMP, func, ForeignKey
from typing import Optional, List, TYPE_CHECKING


if TYPE_CHECKING:
    from .song import Song

class Playlist(Base):
    __tablename__ = "playlists"

    playlist_id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(300))
    genre: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=True)

   
    songs: Mapped[List["Song"]] = relationship(
        secondary="playlist_songs", 
        back_populates="playlists"
    )