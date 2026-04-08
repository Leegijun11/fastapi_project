from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession 
from backend.schemas.user import UserCreate,UserLogin,UserUpdate,UserRead
from backend.service.user import UserService
from backend.database import get_db 
from backend.auth import set_auth_cookies
from backend.auth import get_current_user

router = APIRouter(prefix="/users", tags=["User API"])

@router.post("/signup")  # 회원가입
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await UserService.signup(db, user)

@router.post("/login")  # 로그인
async def login(user: UserLogin, response: Response, db: AsyncSession = Depends(get_db)):
    db_user, access_token, refresh_token = await UserService.login(db, user)
    set_auth_cookies(response, access_token, refresh_token)
    return {"user": db_user}

@router.get("/")  # 전체 조회
async def get_all_users(db: AsyncSession = Depends(get_db),
                  current_user= Depends(get_current_user)):
    return await UserService.get_user_all(db,current_user.user_id)

@router.get("/{user_id}")  # 특정 조회
async def get_user(user_id: int, db: AsyncSession = Depends(get_db),
                   current_user= Depends(get_current_user)):
    return await UserService.get_user(db, user_id,current_user.user_id)

@router.patch("/{user_id}")  # 수정
async def update_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db),
                    current_user= Depends(get_current_user)):
    return await UserService.update_user(db, user_id, user,current_user.user_id)

@router.delete("/{user_id}")  # 삭제
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db),
                      current_user= Depends(get_current_user)):
    return await UserService.delete_user(user_id, db,current_user.user_id)