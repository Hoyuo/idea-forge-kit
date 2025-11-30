from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.routes.auth import router as auth_router
from src.api.routes.messages import read_router, router as messages_router
from src.api.routes.rooms import router as rooms_router
from src.api.routes.status import router as status_router
from src.api.routes.users import router as users_router
from src.core.config import settings
from src.database import engine
from src.models.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: 테이블 생성
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(rooms_router)
app.include_router(messages_router)
app.include_router(read_router)
app.include_router(status_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
