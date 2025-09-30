from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from pathlib import Path
from dotenv import load_dotenv
import logging
from routers import document_routes
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# Create and configure FastAPI app
app = FastAPI()

# Set up environment variables
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")

# Configure upload directory
UPLOAD_DIR = Path("generated_files")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Mount the static files directory
app.mount("/files", StaticFiles(directory=str(UPLOAD_DIR)), name="files")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(document_routes.router)

if __name__ == "__main__":
    # Configure Uvicorn with WebSocket settings
    config = uvicorn.Config(
        app=app,
        host="0.0.0.0",
        port=8000,
        ws_ping_interval=35,
        ws_ping_timeout=45,
    )
    server = uvicorn.Server(config)
    server.run()
