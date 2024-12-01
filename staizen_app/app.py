from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Utility
from utils.logger import logger

# Import Services
from core.routers.google_auth.router import google_services

tags_metadata = [
    {
        "name": "Google Auth Services",
    },
    {
        "name": "Streaming",
    }
]

app = FastAPI(
        title="Staizen API Documentation",
        description="Documentation for Staizen API related services",
        openapi_tags=tags_metadata
        )


app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_headers = ["*"],
    allow_methods = ["*"],
    allow_credentials = True
)


@app.get("/")   
async def read_root_endpoint():
    return {"Hello": "Staizen!"}


# Routers/Endpoints
app.include_router(google_services)


logger.name = 'Root Project'
logger.info('All routes are loaded successfully!')