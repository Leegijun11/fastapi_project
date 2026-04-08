from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from backend.models.review import Review
from backend.schemas.review import ReviewCreate,ReviewResponse,ReviewUpdate
from backend.crud.review import ReviewCrud

class ReviewService:

    @staticmethod
    async def add_review(db:AsyncSession,song_id:int,user_id:int ,review:ReviewCreate):
        try:
            new_review = await ReviewCrud.new_review(db, song_id, review, user_id)
            await db.commit()
            return new_review
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=500, detail="서버 오류로인한 생성 실패")
  
    @staticmethod
    async def update_review(db: AsyncSession, review_id: int, rating: int, comment: str):
        try:        
            review_data = ReviewUpdate(rating=rating, comment=comment)
            db_update_review = await ReviewCrud.update_by_id(review_id, db, review_data)         
            if not db_update_review:
                raise HTTPException(
                    status_code=404, 
                    detail=f"ID {review_id} 리뷰를 찾지 못했습니다."
                )
            await db.commit()
            await db.refresh(db_update_review)       
            return db_update_review
            
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=500, 
                detail=f"서버 오류: {str(e)}"
            )

    @staticmethod
    async def del_review(db:AsyncSession, review_id:int):
        db_del_review = await ReviewCrud.delete_by_id(review_id,db)
        if not db_del_review:
            raise HTTPException(status_code=404, detail="리뷰 삭제 실패. 다시 시도해주세요")
        await db.commit()
        return db_del_review

    @staticmethod
    async def get_review(db:AsyncSession, review_id:int):
        db_get_review = await ReviewCrud.get_by_id(db,review_id)
        if not db_get_review :
            raise HTTPException(status_code=400,detail="해당 리뷰가 없다.")
        return db_get_review

    
    @staticmethod
    async def all_review(db:AsyncSession):
        db_all_review = await ReviewCrud.get_all(db)
        if db_all_review is None:
            raise HTTPException( status_code=500, detail="데이터베이스 조회 중 오류 발생")
        return db_all_review