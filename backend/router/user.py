from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession 
from schemas.user import UserRead, UserLogin, UserUpdate
from service.user import UserService, UserCreate, UserService
from database import get_db 
from auth import set_auth_cookies


router = APIRouter(prefix="/users", tags=["User API"])

#회원가입
@router.post("/",response_model=UserRead)
async def signup(user:UserCreate, db:AsyncSession=Depends(get_db)):
    return await UserService.signup(db, user)

#로그인
@router.post("/")
async def login(user: UserLogin,response:Response, db:AsyncSession=Depends(get_db)):
    db_user,access_token,refresh_token=await UserService.login(db, user)
    set_auth_cookies(response, access_token,refresh_token)
    return {
        "user":db_user,
        "access_token":access_token,
        "refresh_token":refresh_token
    }


#모든 정보 조회
@router.post("/",response_model=list[UserRead])
async def get_me( db:AsyncSession=Depends(get_db)):
    return await UserService.get_user_all(db)

#특정 사용자 조회
@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id:int, db:AsyncSession=Depends(get_db)):
    return await UserService.get_user(db, user_id)

#수정
@router.get("/{user_id}",response_model=UserRead)
async def update_user(
    user_id:int,
    user:UserUpdate,
    db:AsyncSession=Depends(get_db),
):
    return await UserService.update_user(db,user_id,user)

#삭제
@router.delete("/{user_id}")
async def delete_user(user_id:int, db:AsyncSession=Depends(get_db)):
    return await UserService.delete_user(user_id, db)