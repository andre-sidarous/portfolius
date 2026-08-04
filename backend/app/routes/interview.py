from app.routes.resume import resume_text, job_description
from fastapi import APIRouter

router = APIRouter()

@router.post("/interview/start")
async def start_interview(resume_text: str, job_description: str):
    return {"message": "Interview started", "resume_text": resume_text, "job_description": job_description}

@router.post("/interview/answer")
async def answer_question(resume_text: str, job_description: str, question: str):
    return {"answer": f"Answer to '{question}' based on the provided resume and job description."}

@router.post("/interview/final")
async def final_interview(resume_text: str, job_description: str):
    return {"final_assessment": "Final assessment based on the provided resume and job description."}