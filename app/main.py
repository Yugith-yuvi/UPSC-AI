from fastapi import FastAPI, Form, UploadFile, File
from app.services.mains_evaluator import evaluate_mains_submission
from app.services.csat_solver import solve_csat_question
from app.services.quiz_syllabus import generate_prelims_quiz, get_syllabus_notes
from app.services.ocr_service import extract_text_from_file
from app.db import log_api_activity, log_mains_score, get_score_history

app = FastAPI(title="UPSC AI Engine", version="1.2.0")

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

@app.post("/api/v1/payment/create-order")
def create_payment_order(plan_type: str = Form(...)):
    # Simple order stub for integration testing
    amount_map = {"pro_monthly": 49900, "token_pack": 19900}  # Amounts in paise
    return {
        "status": "created",
        "order_id": "order_mock_12345",
        "amount": amount_map.get(plan_type, 49900),
        "currency": "INR"
    }