from huggingface_hub import InferenceClient
from app.core.config import settings
import base64
import base64


async def generate_image(prompt: str):
    """
    Generate image using HuggingFace Inference API (Flux.1-dev).
    """
    if not settings.HUGGING_FACE_TOKEN:
        raise Exception("HuggingFace Token not configured")
        
    client = InferenceClient(token=settings.HUGGING_FACE_TOKEN)
    
    # Using SDXL
    image = client.text_to_image(
        prompt,
        model="stabilityai/stable-diffusion-xl-base-1.0"
    )

    
    # Convert PIL Image to Bytes
    import io
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # Return as base64 or bytes?
    # Usually better to upload to S3/Local storage and return URL.
    # For now, let's return base64 for simplicity or save locally.
    
    return img_byte_arr

def save_image_locally(image_bytes: bytes, filename: str) -> str:
    import os
    upload_dir = "/app/uploads/images" # Docker volume path
    os.makedirs(upload_dir, exist_ok=True)
    
    file_path = os.path.join(upload_dir, filename)
    with open(file_path, "wb") as f:
        f.write(image_bytes)
        
    return f"/uploads/images/{filename}"
