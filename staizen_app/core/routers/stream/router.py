from fastapi import APIRouter, File, UploadFile, Request, HTTPException, Depends
from fastapi.responses import StreamingResponse
import shutil
from io import BytesIO

# Import services outside the package
from core.auth.auth_handler import verify_current_user
from utils.logger import log_execution_time, logger

# Initialize API rputer related to google auth
stream = APIRouter(prefix='/stream', tags=["Streaming"])

@stream.post(
    "/stream_file",
    summary="Stream different uploaded files"
    )
@log_execution_time
async def upload_download(request: Request, file: UploadFile = File(...), current_user: dict = Depends(verify_current_user)):
    '''
    Endpoint to upload a file and stream it back to the user via StreamingResponse.
    '''
    logger.info(f"File: {file.filename} received!")

    try:
        # Create an in-memory buffer to hold the file
        file_content = BytesIO()
        shutil.copyfileobj(file.file, file_content)
        
        # Reset the buffer's pointer to the beginning
        file_content.seek(0)

        # Stream the file back to the user
        return StreamingResponse(
            file_content, 
            media_type=file.content_type,
            headers={"Content-Disposition": f"attachment; filename={file.filename}"}
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the file: {e}")

    finally:
        await file.close()
