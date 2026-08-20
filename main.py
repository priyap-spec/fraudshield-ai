from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="FraudShield AI")

class Transaction(BaseModel):
    user_id: str
    amount: float
    location: str
    velocity_1hr: int

@app.post("/analyze-risk")
def analyze_transaction(txn: Transaction):
    risk_score = 0
    reasons = []

    if txn.velocity_1hr > 5:
        risk_score += 45
        reasons.append("High transaction velocity detected.")
    if txn.amount > 50000:
        risk_score += 40
        reasons.append("Unusually high transaction amount.")

    if risk_score >= 70:
        action = "BLOCK"
    elif risk_score >= 40:
        action = "CHALLENGE_OTP"
    else:
        action = "APPROVE"

    return {
        "user_id": txn.user_id,
        "risk_score": risk_score,
        "action": action,
        "risk_reasoning": " ".join(reasons) or "Transaction patterns normal."
    }
