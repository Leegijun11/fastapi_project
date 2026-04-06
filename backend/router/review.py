from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.review import ReviewCreate,ReviewUpdate, ReviewResponse
from database import get_db
from service.review import ReviewService

router=APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/{song_id}/review/{user_id}",response_model=int)
async def add_review(response:Response,song_id:int,user_id:int,review:ReviewCreate,db:AsyncSession=Depends(get_db)):
    new_review = await ReviewService.add_review(db,song_id,user_id)
    return {"리뷰 ID",new_review.review_id}
@router.put("/{review_id}",response_model=ReviewResponse)
async def update_review(response:Response,review_id:int,review:ReviewUpdate,db:AsyncSession=Depends(get_db)):
    edit_review = await ReviewService.update_review(db,review_id,review.rating,review.comment)
    return edit_review

@router.delete("/{review_id}")
async def del_review(response:Response,review_id:int,db:AsyncSession=Depends(get_db)):
    await ReviewService.del_review(db,review_id)
    return {"msg":"리뷰가 삭제됨"}

@router.get("/{review_id}",response_model=ReviewResponse)
async def get_review(response:Response,review_id:int,db:AsyncSession=Depends(get_db)):
    my_re = await ReviewService.get_review(db,review_id)
    return my_re

@router.get("/", response_model=list[ReviewResponse]) 
async def all_review(response: Response, db: AsyncSession = Depends(get_db)):
    db_all_re = await ReviewService.all_re(db)
    return db_all_re