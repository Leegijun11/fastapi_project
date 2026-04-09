from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession 
from backend.schemas.user import UserCreate,UserLogin,UserUpdate,UserRead
from backend.service.user import UserService
from backend.database import get_db 
from backend.auth import set_auth_cookies
from backend.auth import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter(prefix="/users", tags=["User API"])

@router.post("/signup")  # 회원가입
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await UserService.signup(db, user)

@router.post("/login")
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    # UserLogin 객체로 변환하지 말고 직접 넘기기
    db_user, access_token, refresh_token = await UserService.login(db, form_data.username, form_data.password)
    set_auth_cookies(response, access_token, refresh_token)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/")  # 전체 조회
async def get_all_users(db: AsyncSession = Depends(get_db),
                  current_user= Depends(get_current_user)):
    return await UserService.get_user_all(db,current_user.user_id)

@router.get("/")  # 특정 조회
async def get_user(db: AsyncSession = Depends(get_db),
                   current_user= Depends(get_current_user)):
    return await UserService.get_user(db,current_user.user_id)

@router.patch("/")  # 수정
async def update_user(user: UserUpdate, db: AsyncSession = Depends(get_db),
                    current_user= Depends(get_current_user)):
    return await UserService.update_user(db,current_user.user_id , user)

@router.delete("/{user_id}")  # 삭제
async def delete_user(user_id:int,db: AsyncSession = Depends(get_db),
                      current_user= Depends(get_current_user)):
    return await UserService.delete_user(current_user.user_id, db,user_id)