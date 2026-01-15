from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy import select, update, func
from datetime import datetime
import json
import asyncio

from app.api import deps
from app.models.chat import Conversation, Message
from app.models.character import Character
from app.schemas.chat import MessageCreate
from app.services.gemini import get_chat_response

router = APIRouter()

@router.post("/")
async def chat_stream(
    request: Request,
    message_in: MessageCreate,
    session: deps.SessionDep,
    current_user: deps.CurrentUser
):
    """
    Chat with character (Streaming SSE).
    """
    # 1. Check Daily Limits (KST)
    selected_model = message_in.model if message_in.model else "gemini-2.5-flash"
    
    # Normalize model name for limit check
    if "EXAONE" in selected_model:
        limit_key = "exaone-236b"
        daily_limit = 1000
    elif "3" in selected_model and "flash" in selected_model:

        limit_key = "gemini-3-flash"
        daily_limit = 30
    else:
        limit_key = "gemini-2.5-flash"
        daily_limit = 300


    from app.utils.date import get_kst_today_start
    from app.models.usage import ApiUsageLog
    
    today_kst = get_kst_today_start()
    
    # Check usage count
    limit_query = select(func.count()).select_from(ApiUsageLog).where(
        ApiUsageLog.user_id == current_user.id,
        ApiUsageLog.model == limit_key,
        ApiUsageLog.used_at >= today_kst
    )
    limit_result = await session.execute(limit_query)
    usage_count = limit_result.scalar() or 0
    
    if usage_count >= daily_limit:
         raise HTTPException(
            status_code=429, 
            detail=f"Daily usage limit exceeded ({limit_key}: {daily_limit})"
        )

    # 2. Conversation Setup
    conversation_id = message_in.conversation_id
    character_id = message_in.character_id
    content = message_in.message or message_in.content

    
    if not character_id and not conversation_id:
        raise HTTPException(status_code=400, detail="Character ID or Conversation ID required")

    conversation = None
    is_new_conversation = False

    # Get or Create Conversation
    if conversation_id:
        result = await session.execute(select(Conversation).where(
            Conversation.id == conversation_id,
           Conversation.user_id == current_user.id
        ))
        conversation = result.scalars().first()
    
    if not conversation:
        if not character_id:
             raise HTTPException(status_code=400, detail="Character ID required for new conversation")
             
        # Create new conversation
        conversation = Conversation(
            user_id=current_user.id,
            character_id=character_id,
            title="New Chat" # Could generate title later
        )
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)
        is_new_conversation = True
        conversation_id = conversation.id

        # Update Chat Count for Character
        await session.execute(
            update(Character)
            .where(Character.id == character_id)
            .values(chat_count=Character.chat_count + 1)
        )
        await session.commit()

    # 2. Save User Message
    user_msg = Message(
        role="USER",
        content=content,
        conversation_id=conversation_id
    )
    session.add(user_msg)
    await session.commit()

    # 3. Prepare AI Context
    # Fetch Character details
    result = await session.execute(select(Character).where(Character.id == conversation.character_id))
    character = result.scalars().first()
    
    # Parse Example Dialogs if JSON
    example_dialogs = character.example_dialogs
    formatted_dialogs = ""
    if example_dialogs:
        try:
             import json
             dialogs_data = json.loads(example_dialogs)
             if isinstance(dialogs_data, list):
                 formatted_dialogs = "\n".join([f"User: {d.get('user','')}\n{character.name}: {d.get('char','')}" for d in dialogs_data])
             else:
                 formatted_dialogs = example_dialogs
        except:
             formatted_dialogs = example_dialogs

    system_instruction = f"""
    You are roleplaying as {character.name}.
    Description: {character.description}
    Personality: {character.personality}
    
    Context:
    {character.secret if character.secret else ""}
    {character.worldview.description if character.worldview else ""}
    
    Tone/Style:
    {formatted_dialogs}
    
    Reply naturally as the character. Do not break character.
    """

    # 4. Stream Response
    async def event_generator():
        # First, send the conversation ID
        init_data = json.dumps({"conversationId": conversation_id})
        yield f"data: {init_data}\n\n"
        
        full_response = ""
        try:
            # Call AI Service with Model
            model_slug = limit_key # Log the standardized slug
            async for chunk in get_chat_response([{"role": "user", "content": content}], system_instruction, selected_model):
                full_response += chunk
                data = json.dumps({"text": chunk})
                yield f"data: {data}\n\n"
                
            # Signal Done with conversation ID for frontend sync
            done_data = json.dumps({"done": True, "conversationId": conversation_id})
            yield f"data: {done_data}\n\n"
            
            # 5. Save AI Message & Usage
            if full_response:
                from app.db.session import AsyncSessionLocal
                from app.models.usage import ApiUsageLog
                
                async with AsyncSessionLocal() as session_save:
                     # Save Message
                     ai_msg = Message(
                        role="ASSISTANT",
                        content=full_response,
                        conversation_id=conversation_id
                     )
                     session_save.add(ai_msg)
                     
                     # Log Usage
                     usage_log = ApiUsageLog(
                         user_id=current_user.id,
                         model=model_slug
                     )
                     session_save.add(usage_log)
                     
                     await session_save.commit()


        except Exception as e:
            print(f"Error generating response: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.get("/{conversation_id}/messages")
async def read_chat_messages(
    conversation_id: str,
    session: deps.SessionDep,
    current_user: deps.CurrentUser
) -> Any:
    """
    Get messages for a conversation.
    """
    # Verify ownership
    result = await session.execute(select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ))
    conversation = result.scalars().first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    # Validated: Fetch Messages
    result = await session.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
    )
    messages = result.scalars().all()
    from app.schemas.chat import Message as MessageSchema
    return {"messages": [MessageSchema.model_validate(m).model_dump(by_alias=True) for m in messages]}

@router.delete("/messages/{message_id}")
async def delete_chat_message(
    message_id: str,
    session: deps.SessionDep,
    current_user: deps.CurrentUser
) -> Any:
    """
    Delete a specific message.
    """
    # Need to check ownership via conversation
    result = await session.execute(
        select(Message)
        .join(Conversation)
        .where(Message.id == message_id)
        .where(Conversation.user_id == current_user.id)
    )
    message = result.scalars().first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
        
    await session.delete(message)
    await session.commit()
    return {"status": "success"}


from app.schemas.custom import ImageGenerationRequest

@router.post("/image")
async def generate_chat_image(
    image_in: ImageGenerationRequest,
    session: deps.SessionDep,
    current_user: deps.CurrentUser
):
    """
    Generate image for chat.
    """
    from app.services.huggingface import generate_image, save_image_locally
    from app.models.chat import Message
    import uuid
    
    # Construct prompt from messages
    # Use the last few messages to form context, plus character name
    last_msg = image_in.messages[-1].content if image_in.messages else ""
    
    if not last_msg:
        raise HTTPException(status_code=400, detail="No message content to visualize")
        
    conversation_id = image_in.conversation_id

    
    try:
        # 1. Fetch character context from DB
        character_context = f"{image_in.character_name} in a scene" 
        
        if conversation_id:
            # Get character ID from conversation
            result_conv = await session.execute(
                select(Conversation).where(Conversation.id == conversation_id)
            )
            conversation = result_conv.scalars().first()
            
            if conversation:
                # Get character description
                result_char = await session.execute(
                    select(Character).where(Character.id == conversation.character_id)
                )
                character = result_char.scalars().first()
                if character:
                    character_context = character.description

        # 2. Enhance Prompt
        enhanced_prompt = f"masterpiece, best quality, {character_context}, {last_msg}, anime style, detailed webtoon style illustration"
        
        # 3. Generate Image
        image_bytes = await generate_image(enhanced_prompt)
        
        # 4. Save Image
        filename = f"{uuid.uuid4()}.png"
        image_url = save_image_locally(image_bytes, filename)
        
        # 5. Save Message to DB (if conversation exists)
        if conversation_id:
             msg = Message(
                role="ASSISTANT",
                content=f"![Generated Image]({image_url})", # Special format for frontend
                conversation_id=conversation_id
             )
             session.add(msg)
             await session.commit()
             
        return {"imageUrl": image_url}

    except Exception as e:
        print(f"Image generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Validation needed: Saving AI message inside streaming response requires careful session handling.
# Correction: In FastAPI, BackgroundTasks run AFTER response. But for streaming, we want to save content generated.
# We will use a small hack: create a new session inside the generator (or pass one if thread-safe).
# Since AsyncSession is not thread-safe and bound to request context...
# Let's fix the saving logic in the next step.
