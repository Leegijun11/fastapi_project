from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas.review import ReviewCreate,ReviewUpdate, ReviewResponse
from backend.database import get_db
from backend.service.review import ReviewService
from backend.auth import get_current_user
router=APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/{song_id}/review/{user_id}")
async def add_review(response: Response, song_id: int, user_id: int, review: ReviewCreate, db: AsyncSession = Depends(get_db),
                     current_user= Depends(get_current_user)):
    new_review = await ReviewService.add_review(db, song_id, user_id, review,current_user.user_id)
    return new_review
@router.put("/{review_id}",response_model=ReviewResponse)
async def update_review(response:Response,review_id:int,review:ReviewUpdate,db:AsyncSession=Depends(get_db),
                        current_user= Depends(get_current_user)):
    edit_review = await ReviewService.update_review(db,review_id,review.rating,review.comment,current_user.user_id)
    return edit_review

@router.delete("/{review_id}")
async def del_review(response:Response,review_id:int,db:AsyncSession=Depends(get_db),
                     current_user= Depends(get_current_user)):
    await ReviewService.del_review(db,review_id,current_user.user_id)
    return {"msg":"리뷰가 삭제됨"}

@router.get("/{review_id}")
async def get_review(response:Response,review_id:int,db:AsyncSession=Depends(get_db),
                     current_user= Depends(get_current_user)):
    my_re = await ReviewService.get_review(db,review_id,current_user.user_id)
    return my_re

@router.get("/") 
async def all_review(response: Response, db: AsyncSession = Depends(get_db),
                     current_user= Depends(get_current_user)):
    db_all_re = await ReviewService.all_review(db,current_user.user_id)
    return db_all_re