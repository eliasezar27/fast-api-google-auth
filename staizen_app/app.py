from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Utility
from utils.logger import logger

# Import routers
from core.routers.google_auth.router import google_services
from core.routers.stream.router import stream

# Define tags
tags_metadata = [
    {
        "name": "Google Auth Services",
    },
    {
        "name": "Streaming",
    }
]

# Instantiate Fast API app
app = FastAPI(
        title="Staizen API Documentation",
        description="Documentation for Staizen API related services",
        openapi_tags=tags_metadata
        )

# Setup middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_headers = ["*"],
    allow_methods = ["*"],
    allow_credentials = True
)

# Define root
@app.get("/")   
async def read_root_endpoint():
    return {"Hello": "Staizen!"}


# Expose API routers
app.include_router(google_services)
app.include_router(stream)


# Log start of program
logger.name = 'Root Project'
logger.info('All routes are loaded successfully!')