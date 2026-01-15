import aiohttp
import json
from app.core.config import settings

# OpenAI Compatible Base URL for Gemini
OPENAI_COMPAT_URL = "https://generativelanguage.googleapis.com/v1beta/openai/v1/chat/completions"
# FriendliAI Base URL
FRIENDLI_URL = "https://api.friendli.ai/serverless/v1/chat/completions"

async def get_chat_response(messages: list, character_context: str, model_name: str = "Gemini 2.5 Flash"):
    """
    Generator for chat response using OpenAI-compatible REST APIs.
    Supports Gemini and FriendliAI (EXAONE).
    """
    
    # Selection logic
    is_exaone = "EXAONE" in model_name
    
    if is_exaone:
        if not settings.FRIENDLI_TOKEN:
            yield "FriendliAI Token not configured"
            return
        url = FRIENDLI_URL
        api_key = settings.FRIENDLI_TOKEN
        api_model = "LGAI-EXAONE/K-EXAONE-236B-A23B"
    else:
        if not settings.GEMINI_API_KEY:
            yield "Gemini API Key not configured"
            return
        url = OPENAI_COMPAT_URL
        api_key = settings.GEMINI_API_KEY
        # Model Mapping for Gemini
        api_model = "gemini-2.0-flash-exp"
        if model_name == "Gemini 2.5 Flash":
            api_model = "gemini-2.0-flash-exp"
        elif model_name == "Gemini 3.0 Flash":
            api_model = "gemini-1.5-pro"
        
    # Headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # OpenAI Style Payload
    openai_messages = [{"role": "system", "content": character_context}]
    for msg in messages:
        role = msg.get('role', 'user').lower()
        if role == 'model': role = 'assistant'
        openai_messages.append({
            "role": role,
            "content": msg.get('content', '')
        })
    
    payload = {
        "model": api_model,
        "messages": openai_messages,
        "temperature": 0.9,
        "max_tokens": 1000,
        "stream": True
    }
    
    # Special parameters for EXAONE
    if is_exaone:
        payload.update({
            "parse_reasoning": True,
            "chat_template_kwargs": {
                "enable_thinking": True
            }
        })
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status != 200:
                error_text = await response.text()
                yield f"Error: {response.status} - {error_text}"
                return

            async for line in response.content:
                if line:
                    line_text = line.decode('utf-8').strip()
                    
                    if line_text.startswith("data: "):
                        data_payload = line_text[6:]
                        if data_payload == "[DONE]":
                            break
                            
                        try:
                            data = json.loads(data_payload)
                            delta = data.get("choices", [{}])[0].get("delta", {})
                            
                            # Handle thinking/reasoning if present
                            # Some models put reasoning in reasoning_content
                            reasoning = delta.get("reasoning_content")
                            if reasoning:
                                # We can wrap reasoning in a specific tag for frontend if we want
                                # For now, let's just yield it or skip? 
                                # Let's show it in a block.
                                yield f"<thinking>{reasoning}</thinking>"
                                
                            if "content" in delta:
                                yield delta["content"]
                        except Exception as e:
                            continue


            
    # Note: A proper implementation would use a rigorous JSON stream parser.
    # But for this environment fix, we start here.
