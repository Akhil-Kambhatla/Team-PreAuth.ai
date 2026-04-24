import os
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from dotenv import load_dotenv

from extractor import extract_text
from scorer import score_risk

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index():
    return FileResponse("static/index.html")


@app.post("/analyze")
async def analyze(
    policy_file: UploadFile = File(...),
    medical_record: UploadFile = File(...),
):
    try:
        policy_bytes = await policy_file.read()
        record_bytes = await medical_record.read()

        policy_text = extract_text(policy_bytes)
        record_text = extract_text(record_bytes)

        if len(policy_text.split()) < 40 or len(record_text.split()) < 40:
            return JSONResponse(
                status_code=400,
                content={"error": "One or both documents are too short or unreadable."},
            )

        result = score_risk(policy_text, record_text)
        return result
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"error": "Analysis failed. Please try again."},
        )


@app.post("/analyze-demo")
async def analyze_demo():
    try:
        policy_path = Path("static/demo_policy.pdf")
        record_path = Path("static/demo_record.pdf")

        if not policy_path.exists() or not record_path.exists():
            return JSONResponse(
                status_code=404,
                content={"error": "Demo files not found. Run generate_demo_pdfs.py first."},
            )

        policy_text = extract_text(policy_path.read_bytes())
        record_text = extract_text(record_path.read_bytes())

        if len(policy_text.split()) < 40 or len(record_text.split()) < 40:
            return JSONResponse(
                status_code=400,
                content={"error": "Demo documents could not be read."},
            )

        result = score_risk(policy_text, record_text)
        return result
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"error": "Demo analysis failed. Please try again."},
        )
