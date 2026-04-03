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

class Token(BaseModel): #토큰 JWT
    access_token:str
    token_type:str
    

class UserUpdate(BaseModel): #사용자 수정
    email: Optional[str]=None
    username:Optional[str]=None
    password:Optional[str]=None

class DeleteMessage(BaseModel): #사용자 삭제
    message:str


class UserRead(BaseModel): #특정 사용자 조회
    user_id:int
    username:str
    email:str
    create_at:datetime

    class Config:
        from_attributes=True


class UserMe(BaseModel): #내 정보 조회
    user_id:int
    username:str
    email:str
    created_at:datetime

    class Config:
        from_attributes=True


class UserList(BaseModel): #전체 사용자 조회
    users: list[UserRead]
        


