from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.models.review import Review
from backend.schemas.review import ReviewCreate,ReviewUpdate
from fastapi import HTTPException

class ReviewCrud:
    @staticmethod
    async def new_review(db:AsyncSession,song_id:int,review:ReviewCreate,user_id:int)->Review|None:
        new_review = Review(song_id=song_id, rating=review.rating, comment=review.comment, user_id=user_id)
        db.add(new_review)
        await db.flush()
        return new_review
    
    @staticmethod
    async def get_all(db: AsyncSession) -> list[Review]:
        result = await db.execute(select(Review))
        return result.scalars().all()
    
    @staticmethod
    async def update_by_id(db: AsyncSession,review_id: int, review: ReviewUpdate, user_id: int) -> Review | None:
        update_review = await db.get(Review, review_id)
        
        if not update_review:
            raise HTTPException(status_code=404, detail="리뷰가 없습니다")
        
        if update_review.user_id != user_id:
            raise HTTPException(status_code=403, detail="수정 권한이 없습니다")
        
        update_review.rating = review.rating
        update_review.comment = review.comment
        update_review.user_id = user_id
        await db.flush()
        return update_review
    
    @staticmethod
    async def delete_by_id(db:AsyncSession,review_id:int,user_id:int)->Review|None:
        del_review=await db.get(Review,review_id)

        if not del_review:
            raise HTTPException(status_code=404,detail="리뷰가 없습니다")
        if del_review.user_id != user_id:
            raise HTTPException(status_code=403,detail="삭제 권한이 없습니다")

        await db.delete(del_review)
        await db.flush()
        return {"msg": "리뷰가 삭제됨"}
    
    @staticmethod
    async def get_by_id(db:AsyncSession, review_id:int) -> Review|None:
        result = await db.execute(select(Review).filter(Review.review_id == review_id))
        return result.scalar_one_or_none()