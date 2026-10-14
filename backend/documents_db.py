"""
Personalized Document Checklist Generator for Indian Education Loans.
Categorized into Applicant, Co-applicant, Academic, and Collateral requirements.
"""

from typing import Dict, Any, List

def generate_document_checklist(
    destination: str = "india",
    loan_amount: float = 1000000,
    co_applicant_type: str = "salaried",  # "salaried" | "self_employed" | "farmer_agriculturist"
    has_collateral: bool = False
) -> Dict[str, Any]:
    """Generates an accurate, categorized checklist of documents required by Indian banks."""

    # 1. Student / Applicant Documents
    student_docs = [
        {
            "id": "stu_kyc",
            "name": "Identity & Address Proof (KYC)",
            "details": "Aadhaar Card, Passport, Voter ID or PAN Card (PAN and Aadhaar are mandatory).",
            "mandatory": True
        },
        {
            "id": "stu_academic_records",
            "name": "Past Academic Marksheets & Passing Certificates",
            "details": "10th, 12th, and Graduation semester marksheets and degree certificate.",
            "mandatory": True
        },
        {
            "id": "stu_entrance_score",
            "name": "Entrance Exam Scorecard",
            "details": "Domestic: JEE / CAT / GATE / NEET / CLAT. Abroad: GRE / GMAT / SAT and English tests (IELTS / TOEFL / PTE / Duolingo).",
            "mandatory": True
        },
        {
            "id": "stu_admission_proof",
            "name": "Admission Confirmation & Fee Structure",
            "details": "Official unconditional/conditional admission letter and university-issued breakdown of tuition & living expenses.",
            "mandatory": True
        },
        {
            "id": "stu_photos",
            "name": "Passport Sized Photographs",
            "details": "3 to 4 recent passport-size color photographs of the student.",
            "mandatory": True
        }
    ]

    if destination.lower() == "abroad":
        student_docs.append({
            "id": "stu_abroad_i20_cas",
            "name": "Visa / Form I-20 / CAS / Enrolment Letter",
            "details": "Form I-20 (USA), CAS Letter (UK), Confirmation of Enrolment (Australia), or German University Admit. In-principle sanction can be issued before final visa.",
            "mandatory": True
        })
        student_docs.append({
            "id": "stu_passport_copy",
            "name": "Valid Indian Passport",
            "details": "Clear copies of front and back pages with at least 6 months validity.",
            "mandatory": True
        })

    # 2. Co-applicant / Financial Guarantor Documents
    co_app_docs = [
        {
            "id": "co_kyc",
            "name": "Co-Applicant KYC Documents",
            "details": "PAN Card, Aadhaar Card, Passport/Voter ID, and Electricity Bill / Telephone bill for current address.",
            "mandatory": True
        },
        {
            "id": "co_bank_statements",
            "name": "Bank Account Statements (Last 6 Months)",
            "details": "Salary account statement (if salaried) or primary business operative current/savings account statement with bank seal/stamp.",
            "mandatory": True
        }
    ]

    if co_applicant_type == "salaried":
        co_app_docs.extend([
            {
                "id": "co_salary_slips",
                "name": "Latest 3 Months Salary Slips",
                "details": "Showing gross salary, statutory deductions (PF, TDS), and net pay.",
                "mandatory": True
            },
            {
                "id": "co_form16_itr",
                "name": "Form 16 & Income Tax Returns (Last 2-3 Years)",
                "details": "Form 16 issued by employer and ITR-V acknowledgment copies for past 2 assessment years.",
                "mandatory": True
            },
            {
                "id": "co_employment_id",
                "name": "Employer ID Card / Proof of Employment",
                "details": "Company ID card copy or HR employment verification letter.",
                "mandatory": False
            }
        ])
    elif co_applicant_type == "self_employed":
        co_app_docs.extend([
            {
                "id": "co_business_proof",
                "name": "Business Registration / GST Registration",
                "details": "Shop & Establishment certificate, GST registration certificate, or Partnership Deed / MOA & AOA.",
                "mandatory": True
            },
            {
                "id": "co_itr_computation",
                "name": "ITR with Computation of Income & Audited Financials (Last 3 Years)",
                "details": "Profit & Loss statement, Balance Sheet certified by Chartered Accountant, and tax computation.",
                "mandatory": True
            },
            {
                "id": "co_tds_certificates",
                "name": "Form 26AS / Annual Information Statement (AIS)",
                "details": "Verified tax deduction statement downloaded from Income Tax e-filing portal.",
                "mandatory": False
            }
        ])
    else:  # agriculturist
        co_app_docs.extend([
            {
                "id": "co_land_holding",
                "name": "Agricultural Land Records (7/12 extract / Patta / Chitta / Khasra-Khatauni)",
                "details": "Certified land record extract showing clear ownership and crop cultivation history.",
                "mandatory": True
            },
            {
                "id": "co_tehsildar_income",
                "name": "Income Certificate from Tehsildar / Revenue Authority",
                "details": "Official revenue department certificate declaring annual agricultural income.",
                "mandatory": True
            }
        ])

    # 3. Collateral Documents (If applicable)
    collateral_docs = []
    requires_collateral = loan_amount > 750000 or has_collateral
    if requires_collateral:
        collateral_docs.extend([
            {
                "id": "col_title_deed",
                "name": "Registered Title Deed / Sale Deed",
                "details": "Original registered deed of conveyance in favor of property owner.",
                "mandatory": True
            },
            {
                "id": "col_chain_docs",
                "name": "Prior Title Deeds (Chain of Title for 30 Years)",
                "details": "All linking sale deeds and inheritance documents establishing continuous ownership chain.",
                "mandatory": True
            },
            {
                "id": "col_nec",
                "name": "Non-Encumbrance Certificate (NEC / Nil Encumbrance)",
                "details": "Issued by Sub-Registrar's office for 13 to 30 years confirming property is free of prior mortgages.",
                "mandatory": True
            },
            {
                "id": "col_tax_receipt",
                "name": "Latest Property Tax Paid Receipt & Municipal Approval Plan",
                "details": "Receipt of property tax paid to local municipal corporation or panchayat.",
                "mandatory": True
            },
            {
                "id": "col_fd_alternative",
                "name": "Fixed Deposit / LIC Policy (Alternative Liquid Collateral)",
                "details": "Bank FD receipts or surrender value certificate of LIC insurance policies for lien marking.",
                "mandatory": False
            }
        ])

    # 4. Vidya Lakshmi / Government Application Documents
    application_docs = [
        {
            "id": "app_celaf_form",
            "name": "Vidya Lakshmi CELAF Printout",
            "details": "Common Education Loan Application Form printed after online submission at www.vidyalakshmi.co.in.",
            "mandatory": True
        },
        {
            "id": "app_margin_proof",
            "name": "Proof of Margin Money Contribution",
            "details": "Bank account balance statement or fixed deposit showing student's share of 5% to 15% expenses.",
            "mandatory": True
        }
    ]

    return {
        "destination": destination,
        "loan_amount": loan_amount,
        "requires_collateral": requires_collateral,
        "categories": [
            {
                "category_title": "1. Student / Applicant Documents",
                "icon": "user",
                "items": student_docs
            },
            {
                "category_title": f"2. Co-Applicant / Guarantor Documents ({co_applicant_type.replace('_', ' ').title()})",
                "icon": "users",
                "items": co_app_docs
            },
            {
                "category_title": "3. Collateral & Security Documents",
                "icon": "shield-check",
                "note": "Required for loans above ₹7.5 Lakhs unless studying in a premier listed institute under SBI Scholar / Baroda Scholar.",
                "items": collateral_docs
            },
            {
                "category_title": "4. Bank Application & Portal Forms",
                "icon": "file-text",
                "items": application_docs
            }
        ],
        "total_documents_count": len(student_docs) + len(co_app_docs) + len(collateral_docs) + len(application_docs)
    }
