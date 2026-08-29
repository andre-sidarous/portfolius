from fastapi import APIRouter
from pydantic import BaseModel
from app.config import settings
from google import genai
import json

class InterviewStartRequest(BaseModel):
    resume_text: str
    job_description: str

class AnswerRequest(BaseModel):
    question: str
    answer: str
    job_description: str

class FinalRequest(BaseModel):
    grades: list

router = APIRouter()

@router.post("/start")
async def start_interview(req: InterviewStartRequest):
    try:
        client = genai.Client(api_key=settings.gemini_api_key)
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=f"You are an interview assistant. Use the provided resume and job description to generate 5 interview questions. Only return a JSON object with a 'questions' key containing a list of questions. Do not include any explanations or additional text.\n\nResume:\n{req.resume_text}\n\nJob Description:\n{req.job_description}"
        )
        content = response.text
        return {"questions": json.loads(content).get("questions", [])}
    except Exception as e:
        return {"error": str(e)}

@router.post("/answer")
async def answer_question(req: AnswerRequest):
    try:
        client = genai.Client(api_key=settings.gemini_api_key)
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=f"You are an interview assistant. Use the provided resume, job description, and candidate's answer to evaluate the answer. Return a JSON object with 'evaluation' (string) and 'score' (0-100). Do not include any explanations or additional text.\n\nQuestion: {req.question}\nAnswer: {req.answer}\n\nJob Description:\n{req.job_description}"
        )
        content = response.text
        data = json.loads(content)
        return {"evaluation": data.get("evaluation", ""), "score": data.get("score", 0)}
    except Exception as e:
        return {"error": str(e)}

@router.post("/final")
async def final_interview(req: FinalRequest):
    try:
        client = genai.Client(api_key=settings.gemini_api_key)
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=f"You are an interview assistant. Use the provided grades to generate a final assessment of the candidate. Return a JSON object with 'final_assessment' (string). Do not include any explanations or additional text.\n\nGrades: {req.grades}"
        )
        content = response.text
        return {"final_assessment": json.loads(content).get("final_assessment", "")}
    except Exception as e:
        return {"error": str(e)}