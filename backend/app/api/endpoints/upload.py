from fastapi import APIRouter, HTTPException, Body
import base64
import os
from uuid import uuid4
from app.api import deps
from app.schemas.custom import UploadRequest

router = APIRouter()

@router.post("")
async def upload_file(
    current_user: deps.CurrentUser,
    upload_in: UploadRequest
):
    """
    Upload a file (image) via Base64.
    """
    try:
        # Check if base64 string
        if "," in upload_in.file:
            header, encoded = upload_in.file.split(",", 1)
        else:
            encoded = upload_in.file
            
        # Decode
        data = base64.b64decode(encoded)
        
        # Determine extension (simple check or default to png)
        # In real app, check header or magic bytes
        file_ext = "png" 
        if "jpeg" in upload_in.file or "jpg" in upload_in.file:
             file_ext = "jpg"
        elif "gif" in upload_in.file:
             file_ext = "gif"
             
        filename = f"{uuid4()}.{file_ext}"
        
        # Ensure uploads directory
        os.makedirs("/app/uploads", exist_ok=True)
        file_path = f"/app/uploads/{filename}"
        
        with open(file_path, "wb") as f:
            f.write(data)
            
        return {"url": f"/uploads/{filename}"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
