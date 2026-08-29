from app.utils.pdf_parser import extract_text
from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from google import genai
from app.config import settings
import json

class ScoreRequest(BaseModel):
    resume_text: str
    job_description: str

router = APIRouter()

@router.post("/parse")
async def parse_pdf(file: UploadFile = File(...)):
    file_bytes = await file.read()
    text = extract_text(file_bytes)
    return {"text": text}

@router.post("/score")
async def score_resume(req: ScoreRequest):
    try:
        client = genai.Client(api_key=settings.gemini_api_key)
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=f"You are an ATS resume screener. Return only JSON with ats_score (0-100), strengths (list), gaps (list), and rewrite_suggestions (list). No markdown, no backticks.\n\nResume:\n{req.resume_text}\n\nJob Description:\n{req.job_description}"
        )
        return json.loads(response.text)
    except Exception as e:
        return {"error": str(e)}