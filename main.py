import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import async_engine, Base
from fastapi.concurrency import asynccontextmanager
from dotenv import load_dotenv
# from routers import user, board
# from middleware.token_refresh import TokenRefreshMiddleware

load_dotenv(dotenv_path=".env")

@asynccontextmanager
async def lifespan(app:FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await async_engine.dispose()

app=FastAPI(lifespan=lifespan)
# app.add_middleware(RefreshTokenMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.include_router(user.router)

if __name__=="__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)