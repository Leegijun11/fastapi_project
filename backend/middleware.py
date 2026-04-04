from database import get_db
from fastapi import Request
from jwt_handle import verify_token, create_access_token, create_refresh_token
from crud import UserCrud
from auth import set_auth_cookies
from starlette.middleware.base import BaseHTTPMiddleware
from jwt import ExpiredSignatureError, InvalidTokenError
class TokenRefreshMiddleware(BaseHTTPMiddleware):

    EXCLUDE_PATHS = ["/user/login", "/user/signup"]
    async def dispatch(self, request:Request, call_next):
        if any(request.url.path.startswith(path) for path in self.EXCLUDE_PATHS):
            return await call_next(request)
        response = await call_next(request)

        access_token = request.cookies.get("access_token")
        refresh_token = request.cookies.get("refresh_token")

        if access_token:
            try:
                verify_token(access_token)
                return response
            except (ExpiredSignatureError, InvalidTokenError):
                pass

        if refresh_token:
            try:
                user_id = verify_token(refresh_token)
                new_access_token = create_access_token(user_id)
                new_refresh_token = create_refresh_token(user_id)
                db_gen =get_db()
                db = await anext(db_gen)
                
                try:
                    await UserCrud.update_refresh_token_by_id(db, user_id, new_refresh_token)
                    await db.commit()
                    set_auth_cookies(response, new_access_token, new_refresh_token)
                except Exception:
                    await db.rollback()
                    raise
            
            except(ExpiredSignatureError, InvalidTokenError):
                pass
        return response