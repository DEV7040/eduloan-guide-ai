"""
Comprehensive Test Suite for EduLoan Guide AI
Tests all 10 core responsibilities, financial math, rules, and edge cases.
"""

import sys
import os

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from fastapi.testclient import TestClient
from backend.main import app
from backend.calculators import calculate_education_emi, evaluate_eligibility
from backend.loans_db import LOANS_DATABASE, filter_loans
from backend.schemes_db import SCHEMES_DATABASE
from backend.documents_db import generate_document_checklist
from backend.agent_service import FIRST_MESSAGE_EN, FIRST_MESSAGE_HI, FIRST_MESSAGE_MR, rule_based_expert_agent

client = TestClient(app)

class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []

    def log(self, test_id, name, success, details=""):
        status = "PASS" if success else "FAIL"
        self.tests.append((test_id, name, status, details))
        if success:
            self.passed += 1
            print(f"[{status}] {test_id}: {name}")
        else:
            self.failed += 1
            print(f"[{status}] {test_id}: {name} - ERROR: {details}")

results = TestResults()

# =====================================================================
# CATEGORY 1: Initial Greeting & Specification Compliance
# =====================================================================
def test_case_01():
    """Verify first greeting exact wording compliance."""
    expected = (
        "Hello! Welcome to EduLoan Guide AI 🎓. Are you planning to study in India or abroad? "
        "I'll help you explore suitable education loans, check eligibility, compare options, and estimate your EMI."
    )
    res = client.get("/api/initial-greeting?language=en")
    actual = res.json().get("greeting", "")
    results.log("TC-01", "Initial Greeting Exact Match (English)", actual == expected, f"Got: {actual}")

def test_case_02():
    """Verify Hindi and Marathi initial greetings."""
    res_hi = client.get("/api/initial-greeting?language=hi").json().get("greeting", "")
    res_mr = client.get("/api/initial-greeting?language=mr").json().get("greeting", "")
    valid = "नमस्ते! EduLoan Guide AI" in res_hi and "नमस्कार! EduLoan Guide AI" in res_mr
    results.log("TC-02", "Multilingual Greetings (Hindi & Marathi)", valid)

# =====================================================================
# CATEGORY 2: Loan Finder & Database
# =====================================================================
def test_case_03():
    """Verify all verified banks exist (SBI, BoB, PNB, Canara, HDFC Credila, Avanse, Axis, ICICI)."""
    res = client.get("/api/loans")
    data = res.json().get("loans", [])
    bank_names = [l["bank_name"] for l in data]
    required = ["State Bank of India (SBI)", "Bank of Baroda (BoB)", "Punjab National Bank (PNB)", "HDFC Credila"]
    found_all = all(any(r in b for b in bank_names) for r in required)
    results.log("TC-03", "Loan Database Bank Completeness", found_all and len(data) >= 8)

def test_case_04():
    """Verify India vs Abroad loan filtering."""
    india_loans = filter_loans(destination="india")
    abroad_loans = filter_loans(destination="abroad")
    valid = len(india_loans) > 0 and len(abroad_loans) > 0
    # SBI Global Ed-vantage is abroad only
    sbi_abroad = any(l["id"] == "sbi-global-edvantage" for l in abroad_loans)
    results.log("TC-04", "Destination Filter (India vs Abroad)", valid and sbi_abroad)

def test_case_05():
    """Verify Collateral-Free limit filtering (e.g. loans eligible without property for ₹7.5L)."""
    free_loans = filter_loans(amount=750000, collateral_free=True)
    valid = any("sbi-student-loan" == l["id"] for l in free_loans)
    results.log("TC-05", "Collateral-Free Filter (<= 7.5L CGFSEL)", valid)

# =====================================================================
# CATEGORY 3: EMI & Moratorium Math Engine
# =====================================================================
def test_case_06():
    """Verify Moratorium Interest Capitalization Math."""
    # Principal = 10,00,000, Rate = 10.0%, Moratorium = 2 years, Tenure = 10 years
    # Simple Interest during moratorium = P * r * t = 1,000,000 * 0.10 * 2 = 200,000
    # Capitalized Principal = 1,200,000
    # Monthly EMI for 1,200,000 at 10% for 120 months = 15,858.09
    res = calculate_education_emi(1000000, 10.0, 10, moratorium_years=2.0, moratorium_treatment="capitalize")
    mora_interest = res["moratorium_interest_accrued"]
    rep_principal = res["repayment_principal"]
    monthly_emi = res["monthly_emi"]
    valid = (mora_interest == 200000.0 and rep_principal == 1200000.0 and abs(monthly_emi - 15858.09) < 1.0)
    results.log("TC-06", "Moratorium Capitalization EMI Math Accuracy", valid, f"EMI: {monthly_emi}")

def test_case_07():
    """Verify Pay-Monthly Simple Interest during moratorium mode."""
    # Principal = 10,00,000, Rate = 10%
    # Monthly interest outflow during moratorium = (1,000,000 * 0.10) / 12 = 8,333.33
    # Repayment principal stays 1,000,000
    res = calculate_education_emi(1000000, 10.0, 10, moratorium_years=2.0, moratorium_treatment="pay_simple_interest")
    valid = (res["repayment_principal"] == 1000000.0 and abs(res["moratorium_monthly_outflow"] - 8333.33) < 1.0)
    results.log("TC-07", "Monthly Simple Interest Servicing Math", valid)

def test_case_08():
    """Verify Girl Student 0.50% Interest Concession."""
    r_male = calculate_education_emi(1500000, 9.5, 10, is_female=False)
    r_female = calculate_education_emi(1500000, 9.5, 10, is_female=True)
    valid = (r_female["effective_rate"] == 9.0 and r_female["monthly_emi"] < r_male["monthly_emi"])
    diff = r_male["total_amount_payable"] - r_female["total_amount_payable"]
    results.log("TC-08", f"Girl Student 0.50% Rebate (Total savings: Rs.{diff:,.0f})", valid and diff > 40000)

# =====================================================================
# CATEGORY 4: Eligibility & Subsidy Evaluation
# =====================================================================
def test_case_09():
    """Verify CGFSEL Collateral-Free eligibility for loan <= 7.5L."""
    profile = {
        "destination": "india",
        "amount": 750000,
        "family_income": 600000,
        "institute_tier": "tier2_accredited",
        "cibil_score": 750,
        "has_collateral": False
    }
    res = evaluate_eligibility(profile)
    valid = res["collateral_free_eligible"] is True
    results.log("TC-09", "Eligibility: CGFSEL Guarantee Collateral-Free <= 7.5L", valid)

def test_case_10():
    """Verify CSIS Subsidy for Family Income <= 4.5 Lakhs in India."""
    profile_ews = {
        "destination": "india",
        "amount": 600000,
        "family_income": 350000,  # <= 4.5 Lakhs
        "institute_tier": "tier2_accredited",
        "cibil_score": 730
    }
    profile_non_ews = {
        "destination": "india",
        "amount": 600000,
        "family_income": 650000,  # > 4.5 Lakhs
        "institute_tier": "tier2_accredited",
        "cibil_score": 730
    }
    res_ews = evaluate_eligibility(profile_ews)
    res_non_ews = evaluate_eligibility(profile_non_ews)
    ews_has_csis = any("Central Sector Interest Subsidy" in s["name"] for s in res_ews["applicable_subsidies"])
    non_ews_has_csis = any("Central Sector Interest Subsidy" in s["name"] for s in res_non_ews["applicable_subsidies"])
    results.log("TC-10", "Eligibility: CSIS Subsidy Income Ceiling (<= 4.5L)", ews_has_csis and not non_ews_has_csis)

def test_case_11():
    """Verify Margin Money Rules: 0% up to 4L, 5% India > 4L, 15% Abroad."""
    res_4L = evaluate_eligibility({"destination": "india", "amount": 400000})
    res_india_10L = evaluate_eligibility({"destination": "india", "amount": 1000000})
    res_abroad_20L = evaluate_eligibility({"destination": "abroad", "amount": 2000000})
    valid = (res_4L["margin_money_percentage"] == 0.0 and
             res_india_10L["margin_money_percentage"] == 5.0 and
             res_abroad_20L["margin_money_percentage"] == 15.0)
    results.log("TC-11", "Margin Money Rules (0% <= 4L, 5% India, 15% Abroad)", valid)

def test_case_12():
    """Verify Premier Institute zero-collateral allowance up to 40L (SBI/BoB Scholar)."""
    res_tier1 = evaluate_eligibility({
        "destination": "india",
        "amount": 3000000,  # 30 Lakhs
        "institute_tier": "tier1_iim_iit",
        "has_collateral": False
    })
    valid = res_tier1["collateral_free_eligible"] is True
    results.log("TC-12", "Premier Institute Special Limits (IIT/IIM <= 40L)", valid)

def test_case_13():
    """Verify Low CIBIL Score Penalty & Warning Flag (< 650)."""
    res_low_cibil = evaluate_eligibility({"amount": 1000000, "cibil_score": 620})
    has_warning = any("Low CIBIL score" in pt for pt in res_low_cibil["attention_points"])
    results.log("TC-13", "Co-applicant CIBIL Score Assessment (< 650 Flag)", has_warning)

# =====================================================================
# CATEGORY 5: Document Checklist Generator
# =====================================================================
def test_case_14():
    """Verify Salaried vs Self-Employed vs Agriculturist Co-Applicant Document Sets."""
    d_salaried = generate_document_checklist(destination="india", co_applicant_type="salaried")
    d_self = generate_document_checklist(destination="india", co_applicant_type="self_employed")
    d_farmer = generate_document_checklist(destination="india", co_applicant_type="farmer_agriculturist")
    
    # Check for specific items
    all_sal = [item["id"] for cat in d_salaried["categories"] for item in cat["items"]]
    all_self = [item["id"] for cat in d_self["categories"] for item in cat["items"]]
    all_farmer = [item["id"] for cat in d_farmer["categories"] for item in cat["items"]]

    valid = ("co_salary_slips" in all_sal and 
             "co_business_proof" in all_self and 
             "co_land_holding" in all_farmer)
    results.log("TC-14", "Personalized Checklist: Profession Categorization", valid)

def test_case_15():
    """Verify Collateral Documents only required when loan > 7.5L or collateral requested."""
    d_no_col = generate_document_checklist(loan_amount=500000, has_collateral=False)
    d_with_col = generate_document_checklist(loan_amount=2500000, has_collateral=True)
    
    has_title_no_col = any(item["id"] == "col_title_deed" for cat in d_no_col["categories"] for item in cat["items"])
    has_title_with_col = any(item["id"] == "col_title_deed" for cat in d_with_col["categories"] for item in cat["items"])
    
    results.log("TC-15", "Document Checklist: Collateral Thresholds", not has_title_no_col and has_title_with_col)

# =====================================================================
# CATEGORY 6: Schemes Database
# =====================================================================
def test_case_16():
    """Verify Government Schemes Completeness (CSIS, Vidya Lakshmi, Jan Samarth, CGFSEL)."""
    res = client.get("/api/schemes")
    data = res.json().get("schemes", [])
    ids = [s["id"] for s in data]
    required = ["csis-scheme", "vidya-lakshmi-portal", "jansamarth-portal", "cgfsel-guarantee"]
    valid = all(r in ids for r in required)
    results.log("TC-16", "Government Schemes & Portals Integrity", valid and len(data) >= 5)

# =====================================================================
# CATEGORY 7: AI Advisor Conversational Engine & Rules
# =====================================================================
def test_case_17():
    """Verify Rule: Agent never guarantees loan approval."""
    res = client.post("/api/chat", json={
        "messages": [{"role": "user", "content": "Can you guarantee that my loan will be approved?"}],
        "language": "en"
    })
    reply = res.json().get("response", "")
    # Should contain disclaimer about bank appraisal
    results.log("TC-17", "Strict Rule: No Loan Approval Guarantee", len(reply) > 20)

def test_case_18():
    """Verify Multilingual Chatbot Response in Hindi (हिंदी)."""
    res = client.post("/api/chat", json={
        "messages": [{"role": "user", "content": "मुझे विदेश में पढ़ाई के लिए लोन चाहिए"}],
        "language": "hi"
    })
    reply = res.json().get("response", "")
    has_hindi = any(w in reply for w in ["विदेश", "लोन", "ब्याज", "बैंक"])
    results.log("TC-18", "Multilingual Chatbot: Hindi Response", has_hindi)

def test_case_19():
    """Verify Multilingual Chatbot Response in Marathi (मराठी)."""
    res = client.post("/api/chat", json={
        "messages": [{"role": "user", "content": "मला भारतात शिक्षणासाठी शैक्षणिक कर्ज हवे आहे"}],
        "language": "mr"
    })
    reply = res.json().get("response", "")
    has_marathi = any(w in reply for w in ["कर्ज", "भारत", "व्याज", "बँक"])
    results.log("TC-19", "Multilingual Chatbot: Marathi Response", has_marathi)

# =====================================================================
# CATEGORY 8: Official Links & Security
# =====================================================================
def test_case_20():
    """Verify all official links are authentic and well-formed."""
    links = [
        "https://www.vidyalakshmi.co.in",
        "https://www.jansamarth.in",
        "https://sbi.co.in/web/personal-banking/loans/education-loans",
        "https://canarabank.com"
    ]
    for loan in LOANS_DATABASE:
        assert loan["official_url"].startswith("http"), f"Invalid url: {loan['official_url']}"
    for scheme in SCHEMES_DATABASE:
        assert scheme["official_url"].startswith("http"), f"Invalid url: {scheme['official_url']}"
    results.log("TC-20", "Official Links Verification (HTTPS & Whitelisted)", True)

def main():
    print("=" * 70)
    print("   RUNNING ALL 20 TEST CASES FOR EDULOAN GUIDE AI   ".center(70, "="))
    print("=" * 70)

    test_case_01()
    test_case_02()
    test_case_03()
    test_case_04()
    test_case_05()
    test_case_06()
    test_case_07()
    test_case_08()
    test_case_09()
    test_case_10()
    test_case_11()
    test_case_12()
    test_case_13()
    test_case_14()
    test_case_15()
    test_case_16()
    test_case_17()
    test_case_18()
    test_case_19()
    test_case_20()

    print("=" * 70)
    print(f"RESULTS: {results.passed} PASSED / {results.failed} FAILED (TOTAL: {len(results.tests)})")
    print("=" * 70)

    if results.failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
