"""
Education Loan Financial Mathematics and Eligibility Evaluator Engine.
Accurately models moratorium interest capitalization and RBI/IBA lending rules.
"""

from typing import Dict, Any, List
from .loans_db import LOANS_DATABASE

def calculate_education_emi(
    principal: float,
    annual_rate: float,
    tenure_years: int,
    moratorium_years: float = 2.5,
    moratorium_treatment: str = "capitalize",  # "capitalize" | "pay_simple_interest" | "none"
    is_female: bool = False
) -> Dict[str, Any]:
    """
    Calculates Education Loan EMI with detailed moratorium accounting.
    """
    # Apply 0.50% girl student concession if applicable
    effective_rate = max(1.0, annual_rate - (0.50 if is_female else 0.0))
    monthly_r = (effective_rate / 100.0) / 12.0
    tenure_months = tenure_years * 12
    moratorium_months = int(moratorium_years * 12)

    # Calculate accrued simple interest during study + grace period
    # In Indian banking: Simple Interest = P * r * t (years)
    moratorium_interest = principal * (effective_rate / 100.0) * moratorium_years

    if moratorium_treatment == "capitalize":
        # Accrued interest is added to the principal to form starting repayment principal
        repayment_principal = principal + moratorium_interest
        moratorium_monthly_outflow = 0.0
    elif moratorium_treatment == "pay_simple_interest":
        # Student or parent pays simple interest monthly during moratorium
        repayment_principal = principal
        moratorium_monthly_outflow = (principal * (effective_rate / 100.0)) / 12.0
    else:  # none / immediate
        repayment_principal = principal
        moratorium_interest = 0.0
        moratorium_monthly_outflow = 0.0

    # Amortization formula: EMI = P * r * (1+r)^n / ((1+r)^n - 1)
    if monthly_r > 0 and tenure_months > 0:
        factor = (1.0 + monthly_r) ** tenure_months
        monthly_emi = repayment_principal * monthly_r * factor / (factor - 1.0)
    else:
        monthly_emi = repayment_principal / max(1, tenure_months)

    total_emi_paid = monthly_emi * tenure_months
    total_repayment = (
        total_emi_paid + (moratorium_interest if moratorium_treatment == "pay_simple_interest" else 0.0)
    )
    total_interest_paid = total_repayment - principal

    # Generate yearly summary (first 10 years or full tenure)
    yearly_schedule = []
    balance = repayment_principal
    for year in range(1, min(tenure_years + 1, 16)):
        interest_for_year = 0.0
        principal_for_year = 0.0
        for _ in range(12):
            if balance <= 0:
                break
            month_interest = balance * monthly_r
            month_principal = min(balance, monthly_emi - month_interest)
            balance -= month_principal
            interest_for_year += month_interest
            principal_for_year += month_principal

        yearly_schedule.append({
            "year": year,
            "principal_paid": round(principal_for_year, 2),
            "interest_paid": round(interest_for_year, 2),
            "ending_balance": max(0.0, round(balance, 2))
        })

    # Calculate potential saving if interest is serviced during moratorium (approx 1% prompt payment rebate)
    prompt_rate = max(1.0, effective_rate - 1.0)
    prompt_monthly_r = (prompt_rate / 100.0) / 12.0
    prompt_factor = (1.0 + prompt_monthly_r) ** tenure_months
    prompt_emi = principal * prompt_monthly_r * prompt_factor / (prompt_factor - 1.0)
    potential_savings = max(0.0, (monthly_emi - prompt_emi) * tenure_months)

    return {
        "requested_principal": round(principal, 2),
        "base_rate": annual_rate,
        "effective_rate": effective_rate,
        "is_female_concession_applied": is_female,
        "tenure_years": tenure_years,
        "tenure_months": tenure_months,
        "moratorium_years": moratorium_years,
        "moratorium_months": moratorium_months,
        "moratorium_treatment": moratorium_treatment,
        "moratorium_monthly_outflow": round(moratorium_monthly_outflow, 2),
        "moratorium_interest_accrued": round(moratorium_interest, 2),
        "repayment_principal": round(repayment_principal, 2),
        "monthly_emi": round(monthly_emi, 2),
        "total_interest_paid": round(total_interest_paid, 2),
        "total_amount_payable": round(total_repayment, 2),
        "yearly_schedule": yearly_schedule,
        "estimated_savings_with_prompt_service": round(potential_savings, 2)
    }


def evaluate_eligibility(profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates loan eligibility based on IBA guidelines, income thresholds, and collateral rules.
    """
    destination = profile.get("destination", "india").lower()
    amount = float(profile.get("amount", 1000000))
    family_income = float(profile.get("family_income", 600000))
    institute_tier = profile.get("institute_tier", "tier2_accredited")
    cibil_score = int(profile.get("cibil_score", 720))
    has_collateral = bool(profile.get("has_collateral", False))
    collateral_value = float(profile.get("collateral_value", 0))
    has_admission = bool(profile.get("has_admission", True))
    is_female = bool(profile.get("is_female", False))

    score = 50
    reasons: List[str] = []
    flags: List[str] = []

    # 1. Admission confirmation
    if has_admission:
        score += 15
        reasons.append("Confirmed admission in recognized institution validates academic intent.")
    else:
        flags.append("In-principle pre-admission sanction is available only with select lenders (e.g. HDFC Credila, SBI Global Ed-vantage).")

    # 2. Institute Tier
    if institute_tier in ["tier1_iim_iit", "abroad_top200"]:
        score += 20
        reasons.append("Top-tier institution qualifies for special collateral-free schemes up to ₹40L-₹50L with premier banks.")
    elif institute_tier in ["tier2_accredited", "abroad_general"]:
        score += 10
        reasons.append("Accredited institution qualifies under standard IBA Model Education Loan guidelines.")
    else:
        score += 0
        flags.append("Non-accredited institutions require thorough university review and higher collateral security.")

    # 3. Credit Score of Co-Applicant
    if cibil_score >= 750:
        score += 15
        reasons.append(f"Excellent co-applicant CIBIL score ({cibil_score}) facilitates faster approval and best interest rates.")
    elif cibil_score >= 680:
        score += 10
        reasons.append(f"Good co-applicant credit score ({cibil_score}) meets public bank thresholds.")
    else:
        score -= 15
        flags.append(f"Low CIBIL score ({cibil_score}) may lead to rejection by public banks. Consider adding a joint financial guarantor with CIBIL > 720.")

    # 4. Collateral & Amount Analysis
    collateral_free_eligible = False
    if amount <= 750000:
        collateral_free_eligible = True
        score += 10
        reasons.append("Loan amount is ≤ ₹7.5 Lakhs: 100% eligible for Collateral-Free loan under CGFSEL guarantee scheme.")
    elif institute_tier in ["tier1_iim_iit"] and amount <= 4000000:
        collateral_free_eligible = True
        score += 10
        reasons.append("Premier institute status grants zero-collateral approval up to ₹40 Lakhs (SBI Scholar / Baroda Scholar).")
    elif destination == "abroad" and amount > 750000 and not has_collateral:
        # Check NBFC unsecured eligibility
        if family_income >= 800000 and cibil_score >= 720:
            collateral_free_eligible = True
            reasons.append("Eligible for Unsecured Abroad Loan up to ₹40-50 Lakhs via specialized NBFCs (HDFC Credila / Avanse).")
        else:
            flags.append(f"For loans above ₹7.5L without collateral, public banks require tangible security. NBFCs require higher co-borrower income (₹8L+ p.a.).")
    elif has_collateral and collateral_value >= amount:
        score += 10
        reasons.append("Adequate tangible collateral provided covers 100%+ loan amount, ensuring smooth processing.")

    # 5. Margin Money Requirement
    if amount <= 400000:
        margin_pct = 0.0
    elif destination == "india":
        margin_pct = 5.0
    else:  # abroad
        margin_pct = 15.0

    margin_inr = round((amount * margin_pct) / 100.0, 2)

    # 6. Government Subsidies Eligibility
    subsidies = []
    if destination == "india" and family_income <= 450000:
        subsidies.append({
            "name": "Central Sector Interest Subsidy (CSIS)",
            "benefit": "100% interest subsidy paid by Govt during moratorium period.",
            "authority": "Ministry of Education"
        })
    if destination == "abroad" and family_income <= 800000:
        subsidies.append({
            "name": "Dr. Ambedkar Central Sector Scheme for OBC/EBC",
            "benefit": "Full interest subsidy on overseas loans during moratorium period.",
            "authority": "Ministry of Social Justice"
        })
    if is_female:
        subsidies.append({
            "name": "Girl Student 0.50% Interest Concession",
            "benefit": "Flat 50 bps reduction on interest rate across tenure.",
            "authority": "Public Sector Banks (SBI, BoB, Canara, PNB)"
        })

    # Normalized score between 20 and 98
    final_score = max(20, min(98, score))
    status = "Strong Approval Probability" if final_score >= 80 else ("Moderate Approval Probability" if final_score >= 60 else "Conditional / Requires Profile Strengthening")

    # Filter matching banks
    matching = []
    for loan in LOANS_DATABASE:
        if destination not in loan["destinations"]:
            continue
        # Check if amount fits
        max_limit = loan.get("max_amount_abroad", loan["max_amount"]) if destination == "abroad" else loan["max_amount"]
        if amount <= max_limit:
            matching.append({
                "id": loan["id"],
                "bank_name": loan["bank_name"],
                "product_name": loan["product_name"],
                "category": loan["category"],
                "indicative_rate": f"{loan['indicative_rate_min']}% - {loan['indicative_rate_max']}%",
                "collateral_requirement": loan["collateral_requirement"],
                "official_url": loan["official_url"]
            })

    return {
        "eligibility_score": final_score,
        "status": status,
        "collateral_free_eligible": collateral_free_eligible,
        "margin_money_percentage": margin_pct,
        "margin_money_amount": margin_inr,
        "strengths": reasons,
        "attention_points": flags,
        "applicable_subsidies": subsidies,
        "matching_banks": matching[:5],
        "vidya_lakshmi_recommended": True
    }
