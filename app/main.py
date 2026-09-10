from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.db import fetch_pyqs
from app.routers import payment
import logging

app = FastAPI(title="UPSC AI Engine", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(payment.router)

@app.get("/")
def read_root():
    return {"status": "online", "system": "UPSC AI Preparation Engine"}

# ----------------- PYQ ENDPOINTS -----------------
@app.get("/api/v1/pyq/subjects")
def get_pyq_subjects():
    return {
        "subjects": [
            "Polity & Governance",
            "Economy",
            "Modern History",
            "Ancient & Medieval History",
            "Art & Culture",
            "Geography",
            "Environment & Ecology",
            "Science & Technology",
            "International Relations"
        ]
    }

@app.get("/api/v1/pyq/fetch")
def api_fetch_pyqs(
    subject: str = "Polity & Governance",
    year_start: int = 2006,
    year_end: int = 2025,
    exam_type: str = "Prelims"
):
    try:
        questions = fetch_pyqs(
            subject=subject,
            year_start=year_start,
            year_end=year_end,
            exam_type=exam_type
        )
        return {"status": "success", "count": len(questions), "data": questions}
    except Exception as e:
        logging.error(f"Error fetching PYQs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))