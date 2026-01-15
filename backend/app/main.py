from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import asyncio
from app.core.config import settings
from app.db.base_class import Base
from app.db.session import engine
# Import all models to ensure they are registered
from app.models import user, chat, character, usage

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )

from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware


# CORS Middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")


@app.get("/health")
async def health_check():
    return {"status": "ok", "framework": "fastapi"}

@app.get("/")
async def root():
    return {"message": "Welcome to Character Chat API (FastAPI)"}

from app.api.api import api_router

app.include_router(api_router, prefix=settings.API_V1_STR)

# Create tables
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup_event():
    await create_tables()

os.makedirs("/app/uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="/app/uploads"), name="uploads")
