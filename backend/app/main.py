from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.resume import router as resume_router

app = FastAPI(title="Resume Builder API", description="API for Resume Builder")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  ##! Change to only accept from the frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume_router)
