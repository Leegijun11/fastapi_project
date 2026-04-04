from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import String, TIMESTAMP, func, ForeignKey, CheckConstraint
from typing import Optional, List, TYPE_CHECKING


class Review(Base):
    __tablename__ = "reviews"
    review_id: Mapped[int] =mapped_column(primary_key=True, index=True, autoincrement=True)    # PK, autoincrement
    song_id: Mapped[int]= mapped_column(ForeignKey("songs.song_id"), nullable=False)      # FK 
    user_id: Mapped[int]= mapped_column(ForeignKey("users.user_id"), nullable=False)       # FK 
    rating: Mapped[int]= mapped_column((CheckConstraint("rating >= 1 AND rating <= 5")))    
    comment: Mapped[str]=mapped_column(String,nullable=True)
    created_at: Mapped[Optional[datetime]]= mapped_column(TIMESTAMP, server_default=func.now(), nullable=True)