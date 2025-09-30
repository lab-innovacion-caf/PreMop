import os
import tempfile
import logging
from fastapi import APIRouter, File, UploadFile, WebSocket, Form
from fastapi.responses import JSONResponse
from datetime import datetime
import shutil
from pathlib import Path
from connections.connection_manager import ConnectionManager
from services.document_service import process_mop

router = APIRouter()
manager = ConnectionManager()

UPLOAD_DIR = Path("generated_files")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    websocket_id = await manager.connect(websocket)
    logging.info(f"WebSocket connection established with ID: {websocket_id}")
    
    await websocket.send_json({
        "type": "connection_established",
        "websocket_id": websocket_id
    })

    try:
        while True:
            data = await websocket.receive_json()
            logging.info(f"Received message from {websocket_id}: {data}")
    except Exception as e:
        logging.error(f"WebSocket error: {e}")
    finally:
        await manager.disconnect(websocket_id)
        logging.info(f"WebSocket connection closed with ID: {websocket_id}")

@router.post("/api/upload")
async def process_file(file: UploadFile = File(...), websocket_id: str = Form(...)):
    logging.info(f"WebSocket ID received in upload: {websocket_id}")
    
    if websocket_id not in manager.active_connections:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "No active WebSocket connection found"
            }
        )

    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name
        
        output_file_path = await process_mop(temp_file_path, websocket_id, manager)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"premop_{timestamp}.docx"
        
        final_path = UPLOAD_DIR / unique_filename
        shutil.copy2(output_file_path, final_path)
        
        download_url = f"/files/{unique_filename}"
        
        return JSONResponse({
            "status": "success",
            "message": "File processed successfully",
            "downloadUrl": download_url
        })
    except Exception as e:
        logging.error(f"Error processing file: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e)
            }
        )
    finally:
        if 'temp_file_path' in locals():
            os.remove(temp_file_path)
        if 'output_file_path' in locals():
            os.remove(output_file_path) 