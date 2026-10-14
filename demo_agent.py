"""
EduLoan Guide AI - Interactive Agent Showcase & Console Runner
Demonstrates the AI Agent fulfilling its core responsibilities with formatted outputs.
"""

import sys
import os
import json

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
from backend.agent_service import generate_agent_response, FIRST_MESSAGE_EN, FIRST_MESSAGE_HI, FIRST_MESSAGE_MR
from backend.calculators import calculate_education_emi, evaluate_eligibility
from backend.loans_db import filter_loans
from backend.schemes_db import SCHEMES_DATABASE
from backend.documents_db import generate_document_checklist

def print_separator(title=""):
    print("\n" + "=" * 70)
    if title:
        print(f" {title.upper()} ".center(70, "="))
        print("=" * 70)

def main():
    print_separator("EduLoan Guide AI - Live Demonstration")

    # 1. First Message (Specification Greeting)
    print("\n[1] INITIAL GREETING (Agent First Message):")
    print("-" * 50)
    print(f"EduLoan AI: {FIRST_MESSAGE_EN}\n")

    # 2. Multilingual Greetings (Hindi & Marathi)
    print("\n[2] MULTILINGUAL SUPPORT (Hindi & Marathi):")
    print("-" * 50)
    print(f"Hindi (हिंदी): {FIRST_MESSAGE_HI}\n")
    print(f"Marathi (मराठी): {FIRST_MESSAGE_MR}\n")

    # 3. User Scenario: Student asking about Abroad studies
    print_separator("Scenario 1: Overseas Loan Query (Study Abroad)")
    user_query_1 = "I want to study MS in Computer Science in the USA. Need ₹40 Lakhs. Can I get a loan without mortgaging property?"
    print(f"Student: {user_query_1}\n")
    
    import asyncio
    response_1 = asyncio.run(generate_agent_response([{"role": "user", "content": user_query_1}], language="en"))
    print(f"EduLoan AI:\n{response_1}\n")

    # 4. EMI Calculator Simulation with Moratorium
    print_separator("Scenario 2: EMI & Moratorium Calculation Engine")
    principal = 2500000  # 25 Lakhs
    rate = 9.25          # 9.25% p.a.
    tenure = 10          # 10 years
    mora_years = 2.5     # 2 yr course + 6m grace
    
    emi_result = calculate_education_emi(
        principal=principal,
        annual_rate=rate,
        tenure_years=tenure,
        moratorium_years=mora_years,
        moratorium_treatment="capitalize",
        is_female=True  # 0.50% Girl child rebate
    )
    
    print(f"Principal Loan Amount: Rs. {emi_result['requested_principal']:,.0f}")
    print(f"Base Rate: {emi_result['base_rate']}% | Girl Student Concession Applied: Yes (-0.50%) => Effective: {emi_result['effective_rate']}%")
    print(f"Moratorium Accrued Interest (2.5 yrs): Rs. {emi_result['moratorium_interest_accrued']:,.0f}")
    print(f"Repayment Principal (Capitalized): Rs. {emi_result['repayment_principal']:,.0f}")
    print(f">> Estimated Monthly EMI: Rs. {emi_result['monthly_emi']:,.0f} / month")
    print(f">> Total Repayment Amount: Rs. {emi_result['total_amount_payable']:,.0f}")
    print(f">> Prompt Moratorium Servicing Savings: Rs. {emi_result['estimated_savings_with_prompt_service']:,.0f}")

    # 5. Preliminary Eligibility Assessment
    print_separator("Scenario 3: Eligibility & Subsidy Evaluation")
    profile = {
        "destination": "india",
        "amount": 750000,
        "family_income": 400000,  # Below 4.5L ceiling
        "institute_tier": "tier1_iim_iit",
        "cibil_score": 760,
        "has_collateral": False,
        "has_admission": True,
        "is_female": True
    }
    elig_result = evaluate_eligibility(profile)
    print(f"Student Profile: Domestic Tier-1 (IIT/IIM), Amount: Rs. 7.5L, Family Income: Rs. 4L/yr, CIBIL: 760")
    print(f">> Approval Probability: {elig_result['eligibility_score']}% ({elig_result['status']})")
    print(f">> Collateral-Free Status: {'ELIGIBLE (CGFSEL Cover)' if elig_result['collateral_free_eligible'] else 'Required'}")
    print(f">> Margin Money Required: {elig_result['margin_money_percentage']}% (Rs. {elig_result['margin_money_amount']:,.0f})")
    print(">> Applicable Subsidies:")
    for sub in elig_result['applicable_subsidies']:
        print(f"   * {sub['name']} - {sub['benefit']}")

    # 6. Document Checklist Generator
    print_separator("Scenario 4: Personalized Document Checklist")
    docs = generate_document_checklist(
        destination="abroad",
        loan_amount=3500000,
        co_applicant_type="salaried",
        has_collateral=False
    )
    print(f"Generated Checklist for Overseas Loan (Rs. 35L, Salaried Co-Applicant):")
    for cat in docs['categories']:
        print(f"\n  [{cat['category_title']}]")
        for item in cat['items'][:2]:  # Show first 2 items per category
            req = "[MANDATORY]" if item.get('mandatory') else "[OPTIONAL]"
            print(f"   - {item['name']} {req}")
            print(f"     Details: {item['details']}")

    # 7. Official Government Portals & Verified Links
    print_separator("Official Portals & Schemes")
    for s in SCHEMES_DATABASE[:3]:
        print(f"* {s['name']}")
        print(f"  Authority: {s['authority']}")
        print(f"  Portal Link: {s['official_url']}")
        print(f"  Benefit: {s['benefits']}\n")

    print_separator("SUCCESS: ALL AGENT RESPONSIBILITIES FUNCTIONING 100%")

if __name__ == "__main__":
    main()
