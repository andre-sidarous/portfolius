from fastapi import APIRouter
from pydantic import BaseModel
from app.config import settings
from groq import Groq
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

@router.post("/interview/start")
async def start_interview(req: InterviewStartRequest):
    try:
        client = Groq(api_key=settings.groq_api_key)
        response = client.chat.completions.create(
            model="groq/compound",
            messages=[
                {"role": "system", "content": "You are an interview assistant. Use the provided resume and job description to generate 5 interview questions. Only return a JSON object with a 'questions' key containing a list of questions. Do not include any explanations or additional text."},
                {"role": "user", "content": f"Resume:\n{req.resume_text}\n\nJob Description:\n{req.job_description}"}
            ]
        )
        content = response.choices[0].message.content
        return {"questions": json.loads(content).get("questions", [])}
    except Exception as e:
        return {"error": str(e)}

@router.post("/interview/answer")
async def answer_question(req: AnswerRequest):
    try:
        client = Groq(api_key=settings.groq_api_key)
        response = client.chat.completions.create(
            model="groq/compound",
            messages=[
                {"role": "system", "content": "You are an interview assistant. Use the provided resume, job description, and candidate's answer to evaluate the answer. Return a JSON object with 'evaluation' (string) and 'score' (0-100). Do not include any explanations or additional text."},
                {"role": "user", "content": f"Question: {req.question}\nAnswer: {req.answer}\n\nJob Description:\n{req.job_description}"}
            ]
        )
        content = response.choices[0].message.content
        data = json.loads(content)
        return {"evaluation": data.get("evaluation", ""), "score": data.get("score", 0)}
    except Exception as e:
        return {"error": str(e)}

@router.post("/interview/final")
async def final_interview(req: FinalRequest):
    try:
        client = Groq(api_key=settings.groq_api_key)
        response = client.chat.completions.create(
                    model="groq/compound",
                    messages=[
                        {"role": "system", "content": "You are an interview assistant. Use the provided grades to generate a final assessment of the candidate. Return a JSON object with 'final_assessment' (string). Do not include any explanations or additional text."},
                        {"role": "user", "content": f"Grades: {req.grades}"}
                    ]
                )
        content = response.choices[0].message.content
        return {"final_assessment": json.loads(content).get("final_assessment", "")}
    except Exception as e:
        return {"error": str(e)}