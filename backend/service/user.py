from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from models.user import User
from schemas.user import UserCreate, UserList, UserLogin, UserMe, UserRead, UserUpdate 
class UserService:
    @staticmethod
    async def signup(db: AsyncSession, user_data: UserCreate):
        """회원가입 로직 
        1. 중복 검사: 이미 가입된 이메일이나 유저네임이 있는지 확인
        2. 보안 처리: 비밀번호를 평문으로 저장하지 않고 해싱
        3. DB 저장: 가공된 데이터를 CRUD를 통해 DB에 기록
        4. 트랜잭션: 성공 시 확정(Commit), 실패 시 취소(Rollback)"""
        pass

    @staticmethod
    async def login(db: AsyncSession, login_data: UserLogin):
        """로그인 로직 (인증 -> 토큰 생성 -> 반환)"""
        # 여기서 생성된 토큰을 나중에 미들웨어/라우터에서 쿠키로 굽는다.
        pass

    @staticmethod
    async def get_user_me(db: AsyncSession, user_id: int):
        """내 정보 조회 (UserMe 스키마 활용)"""
        pass

    @staticmethod
    async def update_user(db: AsyncSession, user_id: int, update_data: UserUpdate):
        """프로필 수정 (비밀번호 변경 시 재해싱 로직 포함)"""
        pass

    @staticmethod
    def auth_create_cookie(response, token: str):
        """(요구사항) 응답 헤더에 쿠키를 설정하는 로직"""
        # response.set_cookie(key="access_token", value=token, ...)
        pass