import os
import shutil
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from email_sender import send_bulk_emails


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app = FastAPI()

# Allow local Vite dev server


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SendRequest(BaseModel):
    subject: str
    body: str


def _validate_ext(filename: str, allowed: set[str]):
    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    return ext in allowed


@app.post("/upload/resume")
async def upload_resume(file: UploadFile = File(...)):
    if not _validate_ext(file.filename, {"pdf"}):
        raise HTTPException(status_code=400, detail="Resume must be a .pdf file")

    max_bytes = 10 * 1024 * 1024  # 10MB
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Resume file is empty")
    if len(content) > max_bytes:
        raise HTTPException(status_code=400, detail="Resume file is too large (max 10MB)")

    dest = UPLOAD_DIR / "resume.pdf"
    dest.write_bytes(content)
    return {"message": "Resume uploaded", "path": str(dest)}


@app.post("/upload/csv")
async def upload_csv(file: UploadFile = File(...)):
    if not _validate_ext(file.filename, {"csv"}):
        raise HTTPException(status_code=400, detail="Recipients must be a .csv file")

    max_bytes = 5 * 1024 * 1024  # 5MB
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="CSV file is empty")
    if len(content) > max_bytes:
        raise HTTPException(status_code=400, detail="CSV file is too large (max 5MB)")

    dest = UPLOAD_DIR / "recipients.csv"
    dest.write_bytes(content)
    return {"message": "CSV uploaded", "path": str(dest)}


@app.post("/send-emails")
async def send_emails(req: SendRequest):
    # req.body/req.subject are already validated by Pydantic, but keep defensive trimming.
    subject = (req.subject or "").strip()
    body = (req.body or "").strip()

    # Provide clearer error messages for the frontend.
    if not subject:
        raise HTTPException(status_code=400, detail="Subject is required")
    if not body:
        raise HTTPException(status_code=400, detail="Body is required")

    resume_path = UPLOAD_DIR / "resume.pdf"
    csv_path = UPLOAD_DIR / "recipients.csv"

    if not resume_path.exists():
        raise HTTPException(status_code=400, detail="Resume not uploaded. Upload resume first.")
    if not csv_path.exists():
        raise HTTPException(status_code=400, detail="Recipients CSV not uploaded. Upload CSV first.")

    # Validate CSV columns early for better UX
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read CSV: {e}")

    required_cols = {"name", "email"}
    missing = required_cols - set(df.columns)
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"CSV missing required columns: {', '.join(sorted(missing))}. Expected: name, email",
        )

    return send_bulk_emails(
        subject=subject,
        body=body,
        resume_path=str(resume_path),
        csv_path=str(csv_path),
    )

