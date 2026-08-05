from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth as auth_router
from app.routes import resume as resume_router
from app.routes import interview as interview_router

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
app.include_router(resume_router.router, prefix="/resume", tags=["resume"])
app.include_router(interview_router.router, prefix="/interview", tags=["interview"])

@app.get("/")
async def main():
    return {"message": "Portfolius API is running!"}

@app.get("/health")
async def health():
    return {"status": "healthy"}