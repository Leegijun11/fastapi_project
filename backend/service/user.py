from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from models.user import User
from schemas.user import UserCreate, UserLogin, UserUpdate,UserRead

from jwt_handle import get_password_hash,verify_password,create_access_token,create_refresh_token
from crud.user import UserCrud

class UserService:
    @staticmethod
    async def signup(db:AsyncSession, user:UserCreate):
        if await UserCrud.get_by_username(db, user.username):
            raise HTTPException(status_code=400,  detail="이미 사용중인 이름이다")
        hash_pw= get_password_hash(user.password) 
        user_create=UserCreate(username=user.username, password=hash_pw, email=user.email)

        try:
            new_user=await UserCrud.new_user(db,user=user_create)
            await db.commit()
            await db.refresh(new_user)
            return new_user
        
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=401, detail="잘못된 이메일 또는 비번이다")

       
    @staticmethod
    async def login(db:AsyncSession, user:UserLogin):
        db_user=await UserCrud.get_by_email(db, user.email)

        #디비에 들어잇는 암호화된 비번과 내가 입력한 비번 확인
        if not db_user or not verify_password(user.password, db_user.password):
            raise HTTPException(status_code=401, detail="잘못된 이메일 또는 비번이다")
        

        refresh_token=create_refresh_token(db_user.user_id)
        access_token=create_access_token(db_user.user_id)

        #db에 리프레시 토큰 저장
        updated_user=await UserCrud.update_refresh_token_by_id(db, db_user.user_id, refresh_token)
        await db.commit()
        await db.refresh(updated_user)
        return updated_user, access_token, refresh_token 

    @staticmethod
    async def get_user(db:AsyncSession, user_id:int) -> User:
        db_user=await UserCrud.get_by_id(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="사용자 찾을 수 없다")
        return db_user
    
    @staticmethod
    async def get_user_all(db:AsyncSession) -> User:
        db_users=await UserCrud.get_all(db)
        if not db_users:
            raise HTTPException(status_code=404, detail="사용자 찾을 수 없다")
        return db_users
    
    @staticmethod
    async def update_user(db:AsyncSession, user_id:int,user:UserUpdate) -> User|None:
        db_update_user = await UserCrud.update_by_id()