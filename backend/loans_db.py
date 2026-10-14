"""
Verified Indian Education Loans Database
Contains public sector banks, private banks, and premier NBFCs.
All figures reflect standard RBI & IBA Model Education Loan Scheme guidelines.
"""

from typing import List, Dict, Any

LOANS_DATABASE: List[Dict[Any, Any]] = [
    {
        "id": "sbi-student-loan",
        "bank_name": "State Bank of India (SBI)",
        "product_name": "SBI Student Loan Scheme",
        "category": "public_bank",
        "destinations": ["india", "abroad"],
        "min_amount": 50000,
        "max_amount": 5000000,  # 50L for India (higher for premier institutes)
        "max_amount_abroad": 15000000,  # 1.5 Cr for abroad under Ed-vantage
        "indicative_rate_min": 8.15,
        "indicative_rate_max": 10.15,
        "rate_benchmark": "EBLR (External Benchmark Linked Lending Rate)",
        "collateral_requirement": "No collateral up to ₹7.5 Lakhs (CGFSEL). Above ₹7.5L: Tangible collateral (residential/commercial property, FD, NSC) required.",
        "collateral_free_limit": 750000,
        "margin_money": "Nil up to ₹4 Lakhs; 5% for India > ₹4L; 15% for Abroad",
        "moratorium_period": "Course duration + 12 months",
        "max_tenure_years": 15,
        "processing_fee": "Nil for India; ₹10,000 + GST for Abroad (refundable upon disbursement under certain schemes)",
        "girl_student_concession": "0.50% interest concession",
        "prompt_servicing_concession": "1.00% concession if interest is served during moratorium",
        "vidya_lakshmi_eligible": True,
        "official_url": "https://sbi.co.in/web/personal-banking/loans/education-loans/student-loan-scheme",
        "key_highlights": [
            "Concession of 0.50% for female students",
            "No collateral or third-party guarantee up to ₹7.5 Lakhs",
            "Co-applicant mandatory (Parents/Guardian/Spouse)",
            "Covered under CSIS Central Sector Interest Subsidy for eligible EWS students"
        ]
    },
    {
        "id": "sbi-scholar-loan",
        "bank_name": "State Bank of India (SBI)",
        "product_name": "SBI Scholar Loan (Premier Institutes)",
        "category": "public_bank",
        "destinations": ["india"],
        "min_amount": 100000,
        "max_amount": 4000000,  # Up to 40L collateral-free for IITs, IIMs, NITs List AA/A
        "indicative_rate_min": 7.95,
        "indicative_rate_max": 9.25,
        "rate_benchmark": "EBLR Linked",
        "collateral_requirement": "100% Collateral-Free for premier institutions (List AA like IIM Ahmedabad, Bangalore, Calcutta; List A up to ₹20-40 Lakhs without tangible collateral).",
        "collateral_free_limit": 4000000,
        "margin_money": "Nil for premier listed institutes",
        "moratorium_period": "Course duration + 12 months",
        "max_tenure_years": 15,
        "processing_fee": "Nil",
        "girl_student_concession": "0.50% interest concession",
        "prompt_servicing_concession": "Applicable as per bank circular",
        "vidya_lakshmi_eligible": True,
        "official_url": "https://sbi.co.in/web/personal-banking/loans/education-loans/scholar-loan-scheme",
        "key_highlights": [
            "Special zero-collateral limits up to ₹40 Lakhs for top tier institutes",
            "Zero margin money requirement",
            "Fast-track sanction through campus tie-ups"
        ]
    },
    {
        "id": "sbi-global-edvantage",
        "bank_name": "State Bank of India (SBI)",
        "product_name": "SBI Global Ed-vantage (Overseas Studies)",
        "category": "public_bank",
        "destinations": ["abroad"],
        "min_amount": 750000,
        "max_amount": 15000000,  # Up to 1.5 Crores
        "indicative_rate_min": 8.65,
        "indicative_rate_max": 10.30,
        "rate_benchmark": "EBLR Linked",
        "collateral_requirement": "Tangible collateral security mandatory (House, Flat, Plot, Term Deposit). Third-party collateral accepted.",
        "collateral_free_limit": 0,
        "margin_money": "15% (Scholarship/assistantship can be counted towards margin)",
        "moratorium_period": "Course duration + 6 months",
        "max_tenure_years": 15,
        "processing_fee": "₹10,000 + GST per application",
        "girl_student_concession": "0.50% interest concession",
        "prompt_servicing_concession": "0.50% concession if interest served in moratorium",
        "vidya_lakshmi_eligible": True,
        "official_url": "https://sbi.co.in/web/personal-banking/loans/education-loans/global-ed-vantage-scheme",
        "key_highlights": [
            "High loan ticket size up to ₹1.5 Crores",
            "Tax benefit under Section 80E of Income Tax Act",
            "Includes tuition, travel expenses, laptop, and living costs abroad"
        ]
    },
    {
        "id": "bob-baroda-scholar",
        "bank_name": "Bank of Baroda (BoB)",
        "product_name": "Baroda Scholar Loan for Premier Institutions",
        "category": "public_bank",
        "destinations": ["india", "abroad"],
        "min_amount": 100000,
        "max_amount": 8000000,  # 80L for abroad top universities, 40L for India
        "indicative_rate_min": 8.10,
        "indicative_rate_max": 9.90,
        "rate_benchmark": "BRLLR (Baroda Repo Linked Lending Rate)",
        "collateral_requirement": "Nil collateral up to ₹40 Lakhs for List of Premier Institutes in India & up to ₹40-75 Lakhs for recognized foreign universities.",
        "collateral_free_limit": 4000000,
        "margin_money": "Nil for premier Indian colleges; 10% for abroad top 100 universities",
        "moratorium_period": "Course period + 12 months",
        "max_tenure_years": 15,
        "processing_fee": "Nil for premier institutes in India; 1% (max ₹10,000) for abroad (refundable)",
        "girl_student_concession": "0.50% interest concession",
        "prompt_servicing_concession": "Up to 1.00% prompt payment discount",
        "vidya_lakshmi_eligible": True,
        "official_url": "https://www.bankofbaroda.in/personal-banking/loans/education-loan/baroda-scholar",
        "key_highlights": [
            "One of the most competitive rate structures for overseas education",
            "Higher collateral-free thresholds for top 300 QS-ranked global universities",
            "Free international debit card with zero issuance charges"
        ]
    },
    {
        "id": "pnb-udaan",
        "bank_name": "Punjab National Bank (PNB)",
        "product_name": "PNB Udaan (Overseas Education Loan)",
        "category": "public_bank",
        "destinations": ["abroad"],
        "min_amount": 400000,
        "max_amount": 10000000,  # Up to 1 Cr
        "indicative_rate_min": 8.55,
        "indicative_rate_max": 10.45,
        "rate_benchmark": "RLLR Linked",
        "collateral_requirement": "Up to ₹7.5 Lakhs: Parent co-obligation + CGFSEL. Above ₹7.5 Lakhs: 100% tangible collateral security with third-party guarantee.",
        "collateral_free_limit": 750000,
        "margin_money": "15% for studies abroad",
        "moratorium_period": "Course duration + 12 months",
        "max_tenure_years": 15,
        "processing_fee": "1% of loan amount (refundable on loan take-up)",
        "girl_student_concession": "0.50% interest concession",
        "prompt_servicing_concession": "Standard bank guidelines",
        "vidya_lakshmi_eligible": True,
        "official_url": "https://www.pnbindia.in/education.html",
        "key_highlights": [
            "Covers passage money (airfare) and living expenses",
            "Available for job-oriented professional and technical graduate/post-graduate courses",
            "No prepayment penalty"
        ]
    },
    {
        "id": "canara-vidya-turan",
        "bank_name": "Canara Bank",
        "product_name": "Canara Vidya Turan",
        "category": "public_bank",
        "destinations": ["india"],
        "min_amount": 50000,
        "max_amount": 4000000,
        "indicative_rate_min": 8.20,
        "indicative_rate_max": 9.85,
        "rate_benchmark": "RLLR Linked",
        "collateral_requirement": "No collateral or third-party guarantee up to ₹7.5 Lakhs. Special non-collateral limits for IIMs/IITs.",
        "collateral_free_limit": 750000,
        "margin_money": "Nil up to ₹4 Lakhs; 5% above ₹4 Lakhs",
        "moratorium_period": "Course period + 1 year",
        "max_tenure_years": 15,
        "processing_fee": "Nil for India",
        "girl_student_concession": "0.50% interest concession",
        "prompt_servicing_concession": "0.50% rebate for servicing interest during moratorium",
        "vidya_lakshmi_eligible": True,
        "official_url": "https://canarabank.com/User_page.aspx?othlink=384",
        "key_highlights": [
            "Designated nodal bank for CSIS (Central Sector Interest Subsidy)",
            "Direct interest subsidy integration with Ministry of Education",
            "Zero loan origination charges for domestic students"
        ]
    },
    {
        "id": "hdfc-credila",
        "bank_name": "HDFC Credila",
        "product_name": "HDFC Credila Specialized Education Loan",
        "category": "nbfc",
        "destinations": ["india", "abroad"],
        "min_amount": 100000,
        "max_amount": 20000000,  # Up to 2 Crores
        "indicative_rate_min": 9.50,
        "indicative_rate_max": 13.25,
        "rate_benchmark": "Credila Benchmark Lending Rate (CBLR)",
        "collateral_requirement": "Unsecured (collateral-free) loans available up to ₹40-50 Lakhs based on GRE/GMAT score, university tier, and co-borrower income. Secured loans for higher amounts.",
        "collateral_free_limit": 4500000,
        "margin_money": "Up to 100% finance of total cost of education (Nil margin money in select programs)",
        "moratorium_period": "Course period + 6-12 months (Simple interest or partial EMI payment during moratorium)",
        "max_tenure_years": 14,
        "processing_fee": "1.0% to 1.5% of loan amount + GST",
        "girl_student_concession": "Custom concession on select profile scores",
        "prompt_servicing_concession": "Flexible repayment structures",
        "vidya_lakshmi_eligible": True,
        "official_url": "https://www.hdfccredila.com",
        "key_highlights": [
            "Sanction before admission (pre-visa disbursement proof available)",
            "High unsecured loan limits without needing house/land mortgage",
            "Doorstep document collection and rapid processing within 5-7 business days",
            "Covers 100% cost including tuition, living, health insurance, and laptop"
        ]
    },
    {
        "id": "axis-bank-education-loan",
        "bank_name": "Axis Bank",
        "product_name": "Axis Bank Prime Education Loan",
        "category": "private_bank",
        "destinations": ["india", "abroad"],
        "min_amount": 50000,
        "max_amount": 7500000,
        "indicative_rate_min": 9.15,
        "indicative_rate_max": 12.50,
        "rate_benchmark": "Repo Linked",
        "collateral_requirement": "Unsecured loans up to ₹40 Lakhs for select prime institutes. Collateral required above ₹40L or for non-listed institutes.",
        "collateral_free_limit": 4000000,
        "margin_money": "Nil for loans up to ₹4 Lakhs; 5% India; 15% Abroad",
        "moratorium_period": "Course period + 6 months",
        "max_tenure_years": 15,
        "processing_fee": "Up to 1% + GST",
        "girl_student_concession": "Discounts on select festival campaigns",
        "prompt_servicing_concession": "Standard terms",
        "vidya_lakshmi_eligible": True,
        "official_url": "https://www.axisbank.com/retail/loans/education-loan",
        "key_highlights": [
            "Quick digital in-principle sanction",
            "Loan disbursement before visa for international admissions",
            "Comprehensive coverage for tuition, living, and exam fees"
        ]
    },
    {
        "id": "icici-bank-education-loan",
        "bank_name": "ICICI Bank",
        "product_name": "ICICI Bank Education Loan for Higher Studies",
        "category": "private_bank",
        "destinations": ["india", "abroad"],
        "min_amount": 100000,
        "max_amount": 10000000,
        "indicative_rate_min": 9.25,
        "indicative_rate_max": 12.00,
        "rate_benchmark": "ICICI I-MCLR / Repo Linked",
        "collateral_requirement": "Unsecured loans up to ₹50 Lakhs for top global/Indian universities. Secured loans up to ₹1 Crore against residential property/FD.",
        "collateral_free_limit": 5000000,
        "margin_money": "Nil for select premier colleges; 5-15% for others",
        "moratorium_period": "Course duration + 6 months",
        "max_tenure_years": 12,
        "processing_fee": "0.75% to 1.00% + GST",
        "girl_student_concession": "0.25% concession on select categories",
        "prompt_servicing_concession": "Available on specific profiles",
        "vidya_lakshmi_eligible": True,
        "official_url": "https://www.icicibank.com/personal-banking/loans/education-loan",
        "key_highlights": [
            "Digital sanction letter within 48 hours for pre-approved customers",
            "Preferential forex rates for tuition wire transfers",
            "Flexible co-borrower options"
        ]
    },
    {
        "id": "avanse-financial-services",
        "bank_name": "Avanse Financial Services",
        "product_name": "Avanse Student Loan (Abroad & Specialized)",
        "category": "nbfc",
        "destinations": ["india", "abroad"],
        "min_amount": 100000,
        "max_amount": 15000000,
        "indicative_rate_min": 10.25,
        "indicative_rate_max": 14.50,
        "rate_benchmark": "Avanse Base Rate",
        "collateral_requirement": "Collateral-free up to ₹50-75 Lakhs based on holistic profile (academic pedigree, university employability, test scores).",
        "collateral_free_limit": 5000000,
        "margin_money": "Up to 100% financing (Zero margin money)",
        "moratorium_period": "Course period + 6 months",
        "max_tenure_years": 15,
        "processing_fee": "1% to 2% of sanctioned amount",
        "girl_student_concession": "Applicable on special corporate drives",
        "prompt_servicing_concession": "Structured flexible repayments",
        "vidya_lakshmi_eligible": True,
        "official_url": "https://www.avanse.com/education-loan",
        "key_highlights": [
            "Holistic evaluation beyond just collateral or parent income",
            "Fastest visa letter generation for US, UK, Canada, Germany, Ireland",
            "Covers executive education and non-traditional STEM & pilot training"
        ]
    }
]


def filter_loans(
    destination: str = None,
    amount: float = None,
    collateral_free: bool = None,
    category: str = None
) -> List[Dict[str, Any]]:
    """Filter loans based on destination, amount, collateral requirement, and category."""
    results = []
    for loan in LOANS_DATABASE:
        if destination and destination.lower() not in [d.lower() for d in loan["destinations"]]:
            continue
        if category and category.lower() != loan["category"].lower():
            continue
        if amount:
            max_limit = loan.get("max_amount_abroad", loan["max_amount"]) if destination == "abroad" else loan["max_amount"]
            if amount > max_limit:
                continue
        if collateral_free and loan["collateral_free_limit"] < (amount or 750000):
            continue
        results.append(loan)
    return results
