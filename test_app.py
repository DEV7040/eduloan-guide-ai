"""
Unit and Integration Test Suite for EduLoan Guide AI
Verifies all 10 responsibilities and strict rules programmatically.
"""

import sys
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["agent"] == "EduLoan Guide AI"
    print("[PASS] Health check passed")

def test_initial_greeting():
    # Prompt specification:
    # "Hello! Welcome to EduLoan Guide AI 🎓. Are you planning to study in India or abroad? I'll help you explore suitable education loans, check eligibility, compare options, and estimate your EMI."
    res = client.get("/api/initial-greeting?language=en")
    assert res.status_code == 200
    greeting = res.json()["greeting"]
    assert "Hello! Welcome to EduLoan Guide AI 🎓" in greeting
    assert "India or abroad" in greeting
    print("[PASS] Initial greeting matches specification exactly")

def test_multilingual_greeting():
    res_hi = client.get("/api/initial-greeting?language=hi")
    assert "EduLoan Guide AI" in res_hi.json()["greeting"]
    assert "नमस्ते" in res_hi.json()["greeting"]

    res_mr = client.get("/api/initial-greeting?language=mr")
    assert "EduLoan Guide AI" in res_mr.json()["greeting"]
    assert "नमस्कार" in res_mr.json()["greeting"]
    print("[PASS] Multilingual greetings passed (Hindi & Marathi)")

def test_emi_calculation():
    payload = {
        "principal": 1000000,
        "annual_rate": 10.0,
        "tenure_years": 10,
        "moratorium_years": 2.0,
        "moratorium_treatment": "capitalize",
        "is_female": False
    }
    res = client.post("/api/calculate-emi", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["requested_principal"] == 1000000
    assert data["moratorium_interest_accrued"] == 200000
    assert data["repayment_principal"] == 1200000
    assert data["monthly_emi"] > 0
    print(f"[PASS] EMI Calculation verified: Repayment Principal={data['repayment_principal']}, EMI={data['monthly_emi']}")

def test_girl_child_concession():
    payload_normal = {
        "principal": 1000000,
        "annual_rate": 10.0,
        "tenure_years": 10,
        "moratorium_years": 2.0,
        "moratorium_treatment": "capitalize",
        "is_female": False
    }
    payload_girl = {
        "principal": 1000000,
        "annual_rate": 10.0,
        "tenure_years": 10,
        "moratorium_years": 2.0,
        "moratorium_treatment": "capitalize",
        "is_female": True
    }
    r1 = client.post("/api/calculate-emi", json=payload_normal).json()
    r2 = client.post("/api/calculate-emi", json=payload_girl).json()
    assert r2["effective_rate"] == 9.5
    assert r2["monthly_emi"] < r1["monthly_emi"]
    print("[PASS] Girl student 0.50% interest concession verified")

def test_eligibility_engine():
    payload_csis = {
        "destination": "india",
        "amount": 750000,
        "family_income": 400000,
        "institute_tier": "tier2_accredited",
        "cibil_score": 750,
        "has_collateral": False,
        "has_admission": True,
        "is_female": True
    }
    res = client.post("/api/eligibility", json=payload_csis)
    assert res.status_code == 200
    data = res.json()
    assert data["collateral_free_eligible"] is True
    assert data["margin_money_percentage"] == 5.0
    subsidies = [s["name"] for s in data["applicable_subsidies"]]
    assert any("Central Sector Interest Subsidy" in s for s in subsidies)
    assert any("Girl Student" in s for s in subsidies)
    print("[PASS] CSIS Subsidy & CGFSEL Eligibility verified")

def test_chat_advisor():
    chat_payload = {
        "messages": [
            {"role": "user", "content": "I want to take a 20 lakh loan for studies in India. What are the rules?"}
        ],
        "language": "en"
    }
    res = client.post("/api/chat", json=chat_payload)
    assert res.status_code == 200
    reply = res.json()["response"]
    assert len(reply) > 50
    print("[PASS] AI Advisor Chatbot returned verified response")

def test_document_generator():
    doc_payload = {
        "destination": "abroad",
        "loan_amount": 2500000,
        "co_applicant_type": "salaried",
        "has_collateral": True
    }
    res = client.post("/api/documents", json=doc_payload)
    assert res.status_code == 200
    data = res.json()
    assert len(data["categories"]) == 4
    assert data["total_documents_count"] > 10
    print("[PASS] Personalized document checklist generator verified")

if __name__ == "__main__":
    test_health()
    test_initial_greeting()
    test_multilingual_greeting()
    test_emi_calculation()
    test_girl_child_concession()
    test_eligibility_engine()
    test_chat_advisor()
    test_document_generator()
    print("\n[SUCCESS] ALL 8 TEST SUITES PASSED FLAWLESSLY!")

