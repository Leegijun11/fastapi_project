from fastapi import Request, Response, HTTPException, Depends
from jwt import ExpiredSignatureError, InvalidTokenError
from backend.settings import settings
from backend.jwt_handle import verify_token
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
from backend.database import get_db
from backend.crud.user import UserCrud 
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")
SECRET_KEY = settings.secret_key
ALGORITHM = settings.jwt_algorithm
def set_auth_cookies(response:Response, access_token:str, refresh_token:str) -> None:
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=int(settings.access_token_expire_seconds),
        secure=False,
        httponly=True,
        samesite="Lax",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=int(settings.refresh_token_expire_seconds),
        secure=False,
        httponly=True,
        samesite="Lax",
    )

async def get_user_id(request:Request) -> int:
    access_token=request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Access_token missing")
 
    try:
        user_id=verify_token(access_token)
        if user_id is None:
            raise HTTPException(status_code=401, detail="no uid")
        return user_id
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access_token expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid Access_token")

async def get_optional(request:Request) -> Optional[int]:
    access_token=request.cookies.get("access_token")
    if not access_token:
        return None
    try:
        return verify_token(access_token)
    except(ExpiredSignatureError,InvalidTokenError ):
        return None
    
async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)  # 이걸 추가해야 스웨거에 자물쇠 뜸
):
    # 쿠키 우선, 없으면 헤더에서
    cookie_token = request.cookies.get("access_token")
    resolved_token = cookie_token or token

    if not resolved_token:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    try:
        payload = jwt.decode(resolved_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("uid")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="토큰이 만료되었습니다.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")
    
    db_user = await UserCrud.get_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    return db_user

async def get_owner(resource_user_id: int, current_user=Depends(get_current_user)):
    if current_user.user_id != resource_user_id:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")
    return current_user