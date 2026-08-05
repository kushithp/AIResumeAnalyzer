import os
import uvicorn
from dotenv import load_dotenv

# Load environment variables from .env file (if present)
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes import router

# Ensure database tables exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Resume Analyzer API",
    description="Backend service for ATS scoring, resume parsing, and AI career recommendations.",
    version="1.0.0"
)

# Configure CORS Middleware
origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173,http://localhost:80"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(router)


@app.get("/")
def health_check():
    """Health check endpoint."""
    return {
        "status": "online",
        "service": "AI Resume Analyzer API",
        "docs": "/docs"
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run("app:app", host=host, port=port, reload=True)
