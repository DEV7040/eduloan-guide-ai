"""
FastAPI Server for EduLoan Guide AI.
Exposes clean RESTful endpoints for the AI Chatbot, Loans Database,
Government Schemes, EMI Calculator, Eligibility Evaluator, and Document Checklists.
"""

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

from .loans_db import LOANS_DATABASE, filter_loans
from .schemes_db import SCHEMES_DATABASE
from .calculators import calculate_education_emi, evaluate_eligibility
from .documents_db import generate_document_checklist
from .agent_service import generate_agent_response, FIRST_MESSAGE_EN, FIRST_MESSAGE_HI, FIRST_MESSAGE_MR

app = FastAPI(
    title="EduLoan Guide AI API",
    description="Intelligent Assistant for Education Loans in India",
    version="1.0.0"
)

# Enable CORS for frontend Vite dev server (and production preview)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    api_key: Optional[str] = None
    language: Optional[str] = "en"  # "en", "hi", "mr"


class EmiRequest(BaseModel):
    principal: float = Field(..., ge=10000, description="Loan amount in INR")
    annual_rate: float = Field(..., ge=1.0, le=25.0, description="Annual interest rate in %")
    tenure_years: int = Field(..., ge=1, le=20, description="Repayment tenure in years")
    moratorium_years: float = Field(2.0, ge=0.0, le=7.0, description="Study + grace period in years")
    moratorium_treatment: str = Field("capitalize", description="capitalize | pay_simple_interest | none")
    is_female: bool = Field(False, description="Apply 0.50% girl student concession")


class EligibilityRequest(BaseModel):
    destination: str = "india"  # "india" | "abroad"
    amount: float = 1000000
    family_income: float = 600000
    institute_tier: str = "tier2_accredited"  # tier1_iim_iit | tier2_accredited | tier3_other | abroad_top200 | abroad_general
    cibil_score: int = 720
    has_collateral: bool = False
    collateral_value: float = 0
    has_admission: bool = True
    is_female: bool = False


class DocumentRequest(BaseModel):
    destination: str = "india"
    loan_amount: float = 1000000
    co_applicant_type: str = "salaried"  # salaried | self_employed | farmer_agriculturist
    has_collateral: bool = False


@app.get("/api/health")
def health_check():
    return {"status": "ok", "agent": "EduLoan Guide AI", "version": "1.0.0"}


@app.get("/api/initial-greeting")
def get_initial_greeting(language: str = Query("en")):
    if language == "hi":
        return {"greeting": FIRST_MESSAGE_HI, "language": "hi"}
    elif language == "mr":
        return {"greeting": FIRST_MESSAGE_MR, "language": "mr"}
    return {"greeting": FIRST_MESSAGE_EN, "language": "en"}


@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    msgs = [{"role": m.role, "content": m.content} for m in req.messages]
    reply = await generate_agent_response(msgs, api_key=req.api_key, language=req.language or "en")
    return {"response": reply}


@app.get("/api/loans")
def get_loans(
    destination: Optional[str] = None,
    amount: Optional[float] = None,
    collateral_free: Optional[bool] = None,
    category: Optional[str] = None
):
    results = filter_loans(
        destination=destination,
        amount=amount,
        collateral_free=collateral_free,
        category=category
    )
    return {"count": len(results), "loans": results}


@app.get("/api/schemes")
def get_schemes():
    return {"count": len(SCHEMES_DATABASE), "schemes": SCHEMES_DATABASE}


@app.post("/api/calculate-emi")
def calculate_emi(req: EmiRequest):
    result = calculate_education_emi(
        principal=req.principal,
        annual_rate=req.annual_rate,
        tenure_years=req.tenure_years,
        moratorium_years=req.moratorium_years,
        moratorium_treatment=req.moratorium_treatment,
        is_female=req.is_female
    )
    return result


@app.post("/api/eligibility")
def check_eligibility(req: EligibilityRequest):
    profile = req.model_dump()
    result = evaluate_eligibility(profile)
    return result


@app.post("/api/documents")
def get_document_checklist(req: DocumentRequest):
    result = generate_document_checklist(
        destination=req.destination,
        loan_amount=req.loan_amount,
        co_applicant_type=req.co_applicant_type,
        has_collateral=req.has_collateral
    )
    return result


import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

DIST_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))

if os.path.exists(DIST_DIR):
    assets_dir = os.path.join(DIST_DIR, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        if full_path.startswith("api"):
            return None
        file_path = os.path.join(DIST_DIR, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(DIST_DIR, "index.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)

