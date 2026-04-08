from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from backend.models.review import Review
from backend.schemas.review import ReviewCreate,ReviewResponse,ReviewUpdate
from backend.crud.review import ReviewCrud

class ReviewService:

    @staticmethod
    async def add_review(db:AsyncSession,song_id:int,user_id:int ,review:ReviewCreate,current_user_id: int):
        if not current_user_id:
            raise HTTPException(status_code=401, detail="로그인이 필요한 서비스입니다.")
        try:
            new_review = await ReviewCrud.new_review(db, song_id, review, user_id)
            await db.commit()
            return new_review
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=500, detail="서버 오류로인한 생성 실패")
  
    @staticmethod
    async def update_review(db: AsyncSession, review_id: int, rating: int, comment: str, current_user_id: int):
        # 1. 리뷰 존재 여부 및 데이터 조회
        db_review = await ReviewCrud.get_by_id(db, review_id)
        if not db_review:
            raise HTTPException(status_code=404, detail="리뷰를 찾을 수 없습니다.")

        # 2. [Owner 체크] 리뷰 작성자와 현재 로그인 유저 비교
        if db_review.user_id != current_user_id:
            raise HTTPException(status_code=403, detail="본인이 작성한 리뷰만 수정할 수 있습니다.")

        try:
            review_data = ReviewUpdate(rating=rating, comment=comment)
            # CRUD 인자 순서 확인 (db, review_id, data)
            updated = await ReviewCrud.update_by_id(db, review_id, review_data)
            await db.commit()
            await db.refresh(updated)
            return updated
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=f"업데이트 중 오류 발생: {str(e)}")
    @staticmethod
    async def del_review(db: AsyncSession, review_id: int, current_user_id: int):
        # 1. 리뷰 조회
        db_review = await ReviewCrud.get_by_id(db, review_id)
        if not db_review:
            raise HTTPException(status_code=404, detail="리뷰를 찾을 수 없습니다.")

        # 2. [Owner 체크]
        if db_review.user_id != current_user_id:
            raise HTTPException(status_code=403, detail="본인의 리뷰만 삭제할 수 있습니다.")

        # 3. 삭제 진행
        await ReviewCrud.delete_by_id(db, review_id)
        await db.commit()
        return {"msg": "리뷰가 삭제되었습니다."}
    @staticmethod
    async def get_review(db:AsyncSession, review_id:int,current_user_id: int):
        if not current_user_id:
            raise HTTPException(status_code=401, detail="로그인이 필요한 서비스입니다.")
        db_get_review = await ReviewCrud.get_by_id(db,review_id)
        if not db_get_review :
            raise HTTPException(status_code=400,detail="해당 리뷰가 없다.")
        return db_get_review

    
    @staticmethod
    async def all_review(db:AsyncSession,current_user_id: int):
        if not current_user_id:
            raise HTTPException(status_code=401, detail="로그인이 필요한 서비스입니다.")
        db_all_review = await ReviewCrud.get_all(db)
        if db_all_review is None:
            raise HTTPException( status_code=500, detail="데이터베이스 조회 중 오류 발생")
        return db_all_review