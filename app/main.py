import os
import razorpay
from fastapi import FastAPI, Form, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.services.mains_evaluator import evaluate_mains_submission
from app.services.csat_solver import solve_csat_question
from app.services.quiz_syllabus import generate_prelims_quiz, get_syllabus_notes
from app.services.ocr_service import extract_text_from_file
from app.db import log_api_activity, log_mains_score, get_score_history

app = FastAPI(title="UPSC AI Engine", version="1.2.0")

# ----------------- CORS MIDDLEWARE -----------------
# Enables Streamlit Cloud frontend to communicate with Render backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- RAZORPAY CLIENT SETUP -----------------
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

razorpay_client = None
if RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET:
    razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

@app.get("/")
def check_health():
    return {"status": "online", "system": "UPSC AI Preparation Engine"}

# ----------------- MAINS EVALUATION ENDPOINTS -----------------
@app.post("/api/v1/mains/evaluate")
def api_evaluate_mains(question: str = Form(...), student_answer: str = Form(...)):
    result = evaluate_mains_submission(question, student_answer)
    log_api_activity("/mains/evaluate", question, result.get("mode", "UNKNOWN"))
    log_mains_score(question, 5.5, result.get("content", ""))
    return result

@app.post("/api/v1/mains/evaluate-file")
async def api_evaluate_mains_file(question: str = Form(...), file: UploadFile = File(...)):
    contents = await file.read()
    extracted_text = extract_text_from_file(contents, file.filename)
    result = evaluate_mains_submission(question, extracted_text)
    result["extracted_text"] = extracted_text
    log_api_activity("/mains/evaluate-file", question, result.get("mode", "UNKNOWN"))
    log_mains_score(question, 5.5, result.get("content", ""))
    return result

# ----------------- CSAT & PRELIMS ENDPOINTS -----------------
@app.post("/api/v1/csat/solve")
def api_solve_csat(question: str = Form(...)):
    result = solve_csat_question(question)
    log_api_activity("/csat/solve", question, result.get("mode", "UNKNOWN"))
    return result

@app.post("/api/v1/quiz/generate")
def api_generate_quiz(topic: str = Form(...)):
    result = generate_prelims_quiz(topic)
    log_api_activity("/quiz/generate", topic, result.get("mode", "UNKNOWN"))
    return result

@app.post("/api/v1/notes/get")
def api_get_notes(topic: str = Form(...)):
    result = get_syllabus_notes(topic)
    log_api_activity("/notes/get", topic, result.get("mode", "UNKNOWN"))
    return result

# ----------------- ANALYTICS & PAYMENTS -----------------
@app.get("/api/v1/analytics/scores")
def api_get_scores():
    return {"history": get_score_history()}

@app.post("/api/v1/payment/create-link")
def create_payment_link(plan_type: str = Form("pro_monthly")):
    if not razorpay_client:
        raise HTTPException(
            status_code=500, 
            detail="Razorpay API credentials are missing in Environment Variables."
        )

    amount_map = {
        "pro_monthly": 49900,  # ₹499 in paise
        "token_pack": 19900    # ₹199 in paise
    }
    
    amount = amount_map.get(plan_type, 49900)

    try:
        payment_data = {
            "amount": amount,
            "currency": "INR",
            "accept_partial": False,
            "description": f"UPSC AI Subscription - {plan_type}",
            "customer": {
                "name": "UPSC Aspirant",
                "email": "user@example.com"
            },
            "notify": {"sms": False, "email": False},
            "reminder_enable": False,
            "callback_url": "https://upsc-ai.streamlit.app/",  # Replace with your exact Streamlit URL
            "callback_method": "get"
        }
        
        link_response = razorpay_client.payment_link.create(payment_data)
        return {
            "status": "success",
            "short_url": link_response["short_url"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))