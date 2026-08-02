from app.utils.pdf_parser import extract_text
from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from openai import OpenAI
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
    client = OpenAI(api_key=settings.openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an ATS resume screener. Return only JSON with ats_score (0-100), strengths (list), gaps (list), and rewrite_suggestions (list)."},
            {"role": "user", "content": f"Resume:\n{req.resume_text}\n\nJob Description:\n{req.job_description}"}
        ],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)