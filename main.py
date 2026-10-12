
import os
import shutil
import tempfile

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pathlib import Path

from ai_code.service import analyze_resume
from schema import ResumeAnalysis

app = FastAPI(title="AI Resume Analyzer")


@app.post("/analyze-resume", response_model=ResumeAnalysis)
def analyze_resume_api(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
):
    if not resume.filename or Path(resume.filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF resume.",
        )

    temp_path = None

    try:
        # Save uploaded PDF temporarily
        with tempfile.NamedTemporaryFile(
            suffix=".pdf",
            delete=False,
        ) as temp_file:
            shutil.copyfileobj(resume.file, temp_file)
            temp_path = temp_file.name

        # Call the service function
        result = analyze_resume(
            resume_path=temp_path,
            job_description=job_description,
        )

        # Return the structured response
        return result

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        )

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Resume analysis failed. Please try again.",
        )

    finally:
        resume.file.close()

        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@app.get("/")
def home():
    return {"message": "Resume Analyzer API is running"}
