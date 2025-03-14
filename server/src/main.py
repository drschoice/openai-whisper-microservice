from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import ENVIRONMENT, IS_DEVELOPMENT
from src.middleware import APIKeyMiddleware
from src.routes.model import router as Model
from src.routes.language import router as Language
from src.routes.miscellaneous import router as Miscellaneous


# Create FastAPI app
app = FastAPI(
    title = "Whisper API",
    description = "OpenAI Whisper automatic speech recognition microservice",
    version = "1.0.0",
)

# Add Middleware
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add API Key middleware (will only enforce for /api/ routes)
app.add_middleware(APIKeyMiddleware) 

# Include routers under /api prefix
app.include_router(Model, prefix="/api")
app.include_router(Language, prefix="/api")
app.include_router(Miscellaneous, prefix="/api")


@app.get("/", status_code=200, tags=["Root"])
async def root():
    """
    Return message from container to check if it is running.
    """
    env_info = f" (Environment: {ENVIRONMENT})"
    return {"detail": f"Whisper API is running{env_info}"}
