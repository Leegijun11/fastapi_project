from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.models.user import User
from backend.schemas.user import UserCreate, UserUpdate



class UserCrud:
    @staticmethod
    async def get_by_id(db:AsyncSession, user_id:int) -> User|None:
        result = await db.execute(select(User).filter(User.user_id == user_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_all(db: AsyncSession) -> list[User]:
        result = await db.execute(select(User))
        return result.scalars().all()

    @staticmethod
    async def new_user(user:UserCreate, db:AsyncSession)->User|None:
        new_user = User(username=user.username,email=user.email, password=user.password)
        db.add(new_user)
        await db.flush()
        return new_user
    
    @staticmethod
    async def update_by_id(user_id:int,user:UserUpdate,db:AsyncSession)->User|None:
        update_user = await db.execute(select(User).filter(User.user_id == user_id))
        updating_user = update_user.scalars().first()
        if updating_user :
            updating_user.username = user.username
            updating_user.email = user.email
            updating_user.password = user.password
            await db.flush()
            return {"username":updating_user.username,
                    "email":updating_user.email,
                    "password":updating_user.password
                    }
        return None
    
    @staticmethod
    async def delete_by_id(user_id:int,db:AsyncSession)->User|None:
        del_user = await db.execute(select(User).filter(User.user_id == user_id))
        del_user = del_user.scalars().first()
        if del_user:
            await db.delete(del_user)
            await db.flush()
            return {"msg": "유저가 삭제됨"}
        return None
    
    @staticmethod
    async def update_refresh_token_by_id(
        db:AsyncSession, user_id:int, refresh_token:str):
        db_user=await db.get(User, user_id)
        if db_user:
            db_user.refresh_token=refresh_token
            await db.flush()
        return db_user
    @staticmethod
    async def get_by_username(db: AsyncSession, username: str) -> User | None:
        result = await db.execute(select(User).filter(User.username == username))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalar_one_or_none()