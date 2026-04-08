from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.models.review import Review
from backend.schemas.review import ReviewCreate,ReviewUpdate


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
    async def update_by_id(review_id: int, db: AsyncSession, review: ReviewUpdate) -> Review | None:
        update_review = await db.get(Review, review_id)
        if update_review:
            update_review.rating = review.rating
            update_review.comment = review.comment
            await db.flush()
            return update_review
        return None
    
    @staticmethod
    async def delete_by_id(review_id:int, db:AsyncSession)->Review|None:
        del_review=await db.get(Review,review_id)
        if del_review:
            await db.delete(del_review)
            await db.flush()
            return {"msg": "리뷰가 삭제됨"}
        return None
    
    @staticmethod
    async def get_by_id(db:AsyncSession, review_id:int) -> Review|None:
        result = await db.execute(select(Review).filter(Review.review_id == review_id))
        return result.scalar_one_or_none()