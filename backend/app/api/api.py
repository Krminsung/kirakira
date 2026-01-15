from fastapi import APIRouter
from app.api.endpoints import auth, characters, conversations, chat, usage, upload

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(characters.router, prefix="/characters", tags=["characters"])
api_router.include_router(conversations.router, prefix="/conversations", tags=["conversations"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(usage.router, prefix="/usage", tags=["usage"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
