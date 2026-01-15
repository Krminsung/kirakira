from datetime import timedelta
import base64
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError # DB Integrity Error

from app.api import deps
from app.core import security
from app.core.config import settings
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserLogin, User as UserSchema

router = APIRouter()

@router.post("/register")

async def register(
    response: Response,
    user_in: UserCreate,
    session: deps.SessionDep
) -> Any:

    """
    Create new user.
    """
    result = await session.execute(select(User).where(User.email == user_in.email))
    if result.scalars().first():
        raise HTTPException(
            status_code=400,
            detail="이 이메일은 이미 등록되어 있습니다."
        )


    
    user = User(
        email=user_in.email,
        name=user_in.name,
        password=security.get_password_hash(user_in.password),
        
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    # Auto-login after register
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    return {"user": UserSchema.model_validate(user).model_dump(by_alias=True)}



@router.post("/login", response_model=Token)
async def login(
    response: Response,
    user_in: UserLogin,
    session: deps.SessionDep
) -> Any:
    """
    Get access token for future requests.
    """
    result = await session.execute(select(User).where(User.email == user_in.email))
    user = result.scalars().first()

    if not user or not user.password: # OAuth users might not have passwords
        raise HTTPException(
            status_code=400,
            detail="이메일 또는 비밀번호가 일치하지 않습니다."
        )

    
    if not security.verify_password(user_in.password, user.password):
        print(f"Login failed for {user_in.email}: Password mismatch")
        raise HTTPException(
            status_code=400,
            detail="이메일 또는 비밀번호가 일치하지 않습니다."
        )




    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    
    # Set Cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.get("/me")
async def read_users_me(
    current_user: deps.CurrentUser
) -> Any:
    """
    Get current user.
    """
    return {"user": UserSchema.model_validate(current_user).model_dump(by_alias=True)}

@router.post("/logout")
async def logout(response: Response):
    """
    Log out by clearing the cookie.
    """
    response.delete_cookie(
        key="access_token",
        path="/",
        secure=True,
        samesite="lax",
        httponly=True
    )
    return {"status": "success"}

# Google OAuth Implementation

import httpx
from fastapi.responses import RedirectResponse

@router.get("/google/login")
async def google_login():
    if not settings.GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=501, detail="Google OAuth not configured")
        
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "response_type": "code",
        "scope": "openid email profile",
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "access_type": "offline",
        "prompt": "consent"
    }
    url = f"https://accounts.google.com/o/oauth2/v2/auth?{'&'.join([f'{k}={v}' for k,v in params.items()])}"
    return RedirectResponse(url)

@router.get("/google/callback")
async def google_callback(
    code: str,
    response: Response,
    session: deps.SessionDep
):
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
         raise HTTPException(status_code=501, detail="Google OAuth not configured")

    # 1. Exchange Code for Token
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
    }
    
    async with httpx.AsyncClient() as client:
        token_res = await client.post(token_url, data=data)
        if token_res.status_code != 200:
             raise HTTPException(status_code=400, detail="Failed to get Google token")
        token_data = token_res.json()
        access_token = token_data.get("access_token")
        
        # 2. Get User Info
        user_info_res = await client.get("https://www.googleapis.com/oauth2/v3/userinfo", headers={"Authorization": f"Bearer {access_token}"})
        if user_info_res.status_code != 200:
             raise HTTPException(status_code=400, detail="Failed to get user info")
        user_info = user_info_res.json()
        
    email = user_info.get("email")
    name = user_info.get("name")
    avatar = user_info.get("picture")
    
    if not email:
         raise HTTPException(status_code=400, detail="Email not found in Google profile")

    # 3. Find or Create User
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    
    if not user:
        # Create new user
        user = User(
            email=email,
            name=name or "Unknown",
            password=None, # OAuth user
            avatar=avatar,
            name_changed=False
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
    
    # 4. Issue JWT & Redirect
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    jwt_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    
    # Redirect to Frontend (Root)
    # Ideally should be FRONTEND_URL from settings, but defaulting to referer or hardcoded for now
    frontend_url = "http://localhost:3003" # Default
    if settings.BACKEND_CORS_ORIGINS:
         # Try to pick the first one
         if isinstance(settings.BACKEND_CORS_ORIGINS, list) and len(settings.BACKEND_CORS_ORIGINS) > 0:
             frontend_url = str(settings.BACKEND_CORS_ORIGINS[0]).rstrip('/')

    redirect = RedirectResponse(url=frontend_url)
    redirect.set_cookie(
        key="access_token",
        value=jwt_token,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    return redirect
import os
from uuid import uuid4
from app.schemas.user import UserUpdateName, UserUpdateAvatar

@router.patch("/name")
async def update_name(
    user_in: UserUpdateName,
    current_user: deps.CurrentUser,
    session: deps.SessionDep
) -> Any:
    # Frontend expects { "user": { ... } }
    if current_user.name_changed:
         # Frontend Logic says it warns about 1 time change, but backend should enforce it?
         # "nameChanged" field exists in model.
         pass
         
    current_user.name = user_in.name
    current_user.name_changed = True
    session.add(current_user)
    await session.commit()
    await session.refresh(current_user)
    return {"user": current_user}

@router.post("/avatar")
async def upload_avatar(
    user_in: UserUpdateAvatar,
    current_user: deps.CurrentUser,
    session: deps.SessionDep
) -> Any:
    # Decode Base64
    try:
        format, imgstr = user_in.imageData.split(';base64,') 
        ext = format.split('/')[-1]
        data = base64.b64decode(imgstr)
        
        # Ensure uploads dir
        os.makedirs("/app/uploads/avatars", exist_ok=True)
        
        filename = f"{current_user.id}_{uuid4()}.{ext}"
        filepath = f"/app/uploads/avatars/{filename}"
        
        with open(filepath, "wb") as f:
            f.write(data)
            
        # Update user avatar URL
        # URL should be served by static handler
        avatar_url = f"/uploads/avatars/{filename}"
        current_user.avatar = avatar_url
        
        session.add(current_user)
        await session.commit()
        
        return {"avatar": avatar_url}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image data")

@router.delete("/account")
async def delete_account(
    current_user: deps.CurrentUser,
    session: deps.SessionDep
) -> Any:
    await session.delete(current_user)
    await session.commit()
    return {"status": "success"}
