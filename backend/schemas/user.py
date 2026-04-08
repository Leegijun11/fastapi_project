from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel): #회원가입
    email:str
    username:str
    password:str

class UserLogin(BaseModel): #로그인
    username:str
    password:str

    
class UserUpdate(BaseModel): #사용자 수정
    email: Optional[str]=None
    username:Optional[str]=None
    password:Optional[str]=None


class UserRead(BaseModel): #특정 사용자 조회
    user_id:int
    username:str
    email:str
    password:str
    refresh_token:str
    create_at:datetime

    class Config:
        from_attributes=True
