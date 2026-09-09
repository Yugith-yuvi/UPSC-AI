from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import os
import razorpay

router = APIRouter(prefix="/payments", tags=["Payments"])

# -------------------------------------------------------------
# 1. Safe Global Client Initialization
# -------------------------------------------------------------
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

razorpay_client = None

if RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET:
    try:
        razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
    except Exception:
        razorpay_client = None


# -------------------------------------------------------------
# 2. Request Data Model
# -------------------------------------------------------------
class OrderRequest(BaseModel):
    amount: int  # Amount in INR (Rupees)


# -------------------------------------------------------------
# 3. Guarded Endpoint Function
# -------------------------------------------------------------
@router.post("/create-order")
def create_payment_order(data: OrderRequest):
    # GUARD CHECK: Verify client exists before calling Razorpay APIs
    if razorpay_client is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Payment Service temporarily offline. Please contact support."
        )

    try:
        # Convert rupees to paise (Razorpay processes payments in paise)
        amount_in_paise = data.amount * 100

        order_payload = {
            "amount": amount_in_paise,
            "currency": "INR",
            "payment_capture": 1
        }

        # Safe to execute because razorpay_client was validated above
        order = razorpay_client.order.create(data=order_payload)
        return {"status": "success", "order": order}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create Razorpay order: {str(e)}"
        )