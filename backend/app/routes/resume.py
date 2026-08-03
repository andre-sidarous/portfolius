from app.utils.pdf_parser import extract_text
from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from groq import Groq
from app.config import settings
import json

class ScoreRequest(BaseModel):
    resume_text: str
    job_description: str

router = APIRouter()

@router.post("/resume/parse")
async def parse_pdf(file: UploadFile = File(...)):
    file_bytes = await file.read()
    text = extract_text(file_bytes)
    return {"text": text}

@router.post("/resume/score")
async def score_resume(req: ScoreRequest):
    try:
        client = Groq(api_key=settings.groq_api_key)
        response = client.chat.completions.create(
            model="groq/compound",
            messages=[
                {"role": "system", "content": "You are an ATS resume screener. Return only JSON with ats_score (0-100), strengths (list), gaps (list), and rewrite_suggestions (list). Respond with only a raw JSON object, no markdown, no backticks, no explanation."},
                {"role": "user", "content": f"Resume:\n{req.resume_text}\n\nJob Description:\n{req.job_description}"}
            ]
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}