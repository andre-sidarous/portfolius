from supabase import create_client
from fastapi import APIRouter, HTTPException
from app.config import settings
from pydantic import BaseModel

router = APIRouter()
supabase = create_client(settings.supabase_url, settings.supabase_key)
supabase_admin = create_client(settings.supabase_url, settings.supabase_service_key)

class AuthRequest(BaseModel):
    email: str
    password: str

@router.post("/signup")
async def signup(req: AuthRequest):
    try:
        response = supabase.auth.sign_up({"email": req.email, "password": req.password})

        supabase_admin.table("profiles").insert({
            "id": response.user.id,
            "email": req.email
        }).execute()

        return {"message": "User signed up successfully", "user": response.user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
async def login(req: AuthRequest):
    try:
        response = supabase.auth.sign_in_with_password({"email": req.email, "password": req.password})
        return {"message": "User logged in successfully", "user": response.user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/logout")
async def logout():
    try:
        response = supabase.auth.sign_out()
        return {"message": "User logged out successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))