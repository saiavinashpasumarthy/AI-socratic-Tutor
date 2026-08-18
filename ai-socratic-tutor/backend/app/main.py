from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.tutor import router as tutor_router


app = FastAPI(
    title="AI Socratic Tutor API",
    description="Backend API for an AI-powered Socratic learning assistant",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(tutor_router)


@app.get("/")
def root():
    return {
        "message": "AI Socratic Tutor API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }