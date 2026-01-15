from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload

from app.api import deps
from app.models.character import Character
from app.models.user import User
from app.schemas.character import Character as CharacterSchema, CharacterCreate, CharacterUpdate

router = APIRouter()

@router.get("/public")
async def read_public_characters(
    session: deps.SessionDep,
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Get public characters.
    """
    query = select(Character).where(Character.visibility == "PUBLIC").options(selectinload(Character.creator)).order_by(desc(Character.created_at)).offset(skip).limit(limit)
    result = await session.execute(query)

    return {"characters": [CharacterSchema.model_validate(c).model_dump(by_alias=True) for c in result.scalars().all()]}

@router.get("/")

async def read_characters(
    session: deps.SessionDep,
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    sort: str = "latest"
) -> Any:
    """
    Retrieve characters.
    """
    query = select(Character)
    
    # Filter by visibility (Public only, unless specific logic added later)
    # For now fetching all public characters
    query = query.where(Character.visibility == "PUBLIC")
    
    # Sorting
    if sort == "popular":
        query = query.order_by(desc(Character.like_count))
    else: # latest
        query = query.order_by(desc(Character.created_at))
        
    query = query.offset(skip).limit(limit)
    
    result = await session.execute(query)
    characters = result.scalars().all()
    # Frontend expects { "characters": [...] } and camelCase
    return {"characters": [CharacterSchema.model_validate(c).model_dump(by_alias=True) for c in characters]}


@router.post("/")

async def create_character(
    *,
    session: deps.SessionDep,
    character_in: CharacterCreate,
    current_user: deps.CurrentUser
) -> Any:
    """
    Create new character.
    """
    obj_data = character_in.model_dump()
    
    # Handle JSON string fields
    import json
    for field in ["example_dialogs", "greetings", "album_images"]:
        if field in obj_data and obj_data[field] is not None and not isinstance(obj_data[field], str):
            obj_data[field] = json.dumps(obj_data[field])

    character = Character(
        **obj_data,
        creator_id=current_user.id
    )

    session.add(character)
    await session.commit()
    
    # Reload with creator info
    result = await session.execute(
        select(Character).where(Character.id == character.id).options(selectinload(Character.creator))
    )
    character = result.scalars().first()
    
    return {"character": CharacterSchema.model_validate(character).model_dump(by_alias=True)}



@router.get("/my")
async def read_my_characters(
    session: deps.SessionDep,
    current_user: deps.CurrentUser,
) -> Any:
    """
    Get current user's characters.
    """
    query = select(Character).where(Character.creator_id == current_user.id).options(selectinload(Character.creator)).order_by(desc(Character.updated_at))
    result = await session.execute(query)

    characters = result.scalars().all()
    # Frontend expects { "characters": [...] }
    return { "characters": [CharacterSchema.model_validate(c).model_dump(by_alias=True) for c in characters] }

@router.delete("/{id}")
async def delete_character(
    id: str,
    session: deps.SessionDep,
    current_user: deps.CurrentUser
) -> Any:
    """
    Delete a character.
    """
    result = await session.execute(select(Character).where(Character.id == id))
    character = result.scalars().first()
    
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
        
    if character.creator_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
        
    await session.delete(character)
    await session.commit()
    return {"status": "success", "message": "Character deleted"}

@router.put("/{id}")
async def update_character(
    *,
    session: deps.SessionDep,
    id: str,
    character_in: CharacterUpdate,
    current_user: deps.CurrentUser,
) -> Any:
    """
    Update a character.
    """
    result = await session.execute(select(Character).where(Character.id == id))
    character = result.scalars().first()
    
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
        
    if character.creator_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
        
    update_data = character_in.model_dump(exclude_unset=True)
    
    # Handle JSON string fields
    import json
    for field in ["example_dialogs", "greetings", "album_images"]:
        if field in update_data and update_data[field] is not None and not isinstance(update_data[field], str):
            update_data[field] = json.dumps(update_data[field])

    for field, value in update_data.items():
        setattr(character, field, value)

        
    session.add(character)
    await session.commit()
    
    # Reload with creator info
    result = await session.execute(
        select(Character).where(Character.id == character.id).options(selectinload(Character.creator))
    )
    character = result.scalars().first()
    
    return {"character": CharacterSchema.model_validate(character).model_dump(by_alias=True)}

@router.get("/{id}")


async def read_character(
    id: str,
    session: deps.SessionDep
) -> Any:
    """
    Get character by ID.
    """
    result = await session.execute(select(Character).where(Character.id == id).options(selectinload(Character.creator)))
    character = result.scalars().first()

    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return {"character": CharacterSchema.model_validate(character).model_dump(by_alias=True)}


# TODO: Add update/delete endpoints if needed for My Page
