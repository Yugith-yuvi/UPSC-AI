import os
import logging
import razorpay
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.db import fetch_pyqs

app = FastAPI(title="UPSC AI Engine", version="1.0.0")

# CORS middleware for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Safe Razorpay Client Setup
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

razorpay_client = None
if RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET:
    try:
        razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
    except Exception:
        razorpay_client = None


class OrderRequest(BaseModel):
    amount: int


class VerifyPaymentRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


@app.get("/")
def read_root():
    return {"status": "online", "system": "UPSC AI Preparation Engine"}


# ----------------- PAYMENT ENDPOINTS -----------------
@app.post("/payments/create-order")
def create_payment_order(data: OrderRequest):
    if razorpay_client is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Payment Service temporarily offline."
        )
    try:
        order = razorpay_client.order.create({
            "amount": data.amount * 100,
            "currency": "INR",
            "payment_capture": 1
        })
        return {"status": "success", "order": order}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/payments/verify-payment")
def verify_payment(data: VerifyPaymentRequest):
    if razorpay_client is None or not RAZORPAY_KEY_SECRET:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Payment verification service temporarily offline."
        )
    try:
        params_dict = {
            'razorpay_order_id': data.razorpay_order_id,
            'razorpay_payment_id': data.razorpay_payment_id,
            'razorpay_signature': data.razorpay_signature
        }
        razorpay_client.utility.verify_payment_signature(params_dict)
        return {"status": "success", "message": "Payment verified successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Verification failed: {str(e)}")


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