"""
Verified Government Subsidies, Schemes and Portals for Education Loans in India.
Source: Ministry of Education (MoE), Ministry of Social Justice & Empowerment, IBA.
"""

from typing import List, Dict, Any

SCHEMES_DATABASE: List[Dict[str, Any]] = [
    {
        "id": "csis-scheme",
        "name": "Central Sector Interest Subsidy Scheme (CSIS)",
        "authority": "Ministry of Education, Government of India",
        "type": "Interest Subsidy",
        "eligibility_summary": "EWS students with annual gross parental/family income up to ₹4.50 Lakhs.",
        "course_scope": "Professional and Technical degree courses in recognized institutions in India only.",
        "benefits": "100% Interest subsidy during the moratorium period (Course Duration + 1 year). The Government pays the interest accumulated during the study period.",
        "max_loan_eligible": "Covers loans under IBA Model Scheme (typically up to ₹7.5 Lakhs to ₹10 Lakhs).",
        "income_ceiling": "₹4,50,000 per annum (income certificate issued by designated state authority mandatory)",
        "nodal_bank": "Canara Bank is the designated nodal agency for CSIS disbursement.",
        "how_to_apply": "Apply through the Vidya Lakshmi Portal (www.vidyalakshmi.co.in) and notify the lending bank during loan sanctioning.",
        "official_url": "https://www.education.gov.in/schemes/higher-education/central-sector-interest-subsidy-scheme",
        "key_notes": [
            "Subsidy applies ONLY for the moratorium period (study duration + 1 year)",
            "Once moratorium ends, borrower pays normal EMI and regular interest",
            "Discontinued for studies abroad; exclusively for domestic professional/technical programs"
        ]
    },
    {
        "id": "vidya-lakshmi-portal",
        "name": "PM Vidyalaxmi / Vidya Lakshmi Portal (CELAF)",
        "authority": "Ministry of Finance & Ministry of Education, Managed by NSDL (Protean)",
        "type": "Single Window Application Platform",
        "eligibility_summary": "All Indian students applying for education loans to public and registered private banks.",
        "course_scope": "Higher education in India and Abroad.",
        "benefits": "Single Common Education Loan Application Form (CELAF). Apply to up to 3 banks and multiple schemes in one single application. Transparent online tracking.",
        "max_loan_eligible": "Varies by bank and institute scheme.",
        "income_ceiling": "No income ceiling for portal registration; specific schemes have their own limits.",
        "nodal_bank": "Managed by Protean eGov Technologies for Indian Banks' Association (IBA).",
        "how_to_apply": "Register at www.vidyalakshmi.co.in -> Fill CELAF -> Search Loans -> Apply to shortlisted banks.",
        "official_url": "https://www.vidyalakshmi.co.in",
        "key_notes": [
            "Official platform mandated by Government of India for bank education loans",
            "Banks are required to process applications within 15-30 days",
            "Integrates directly with National Scholarship Portal (NSP)"
        ]
    },
    {
        "id": "jansamarth-portal",
        "name": "Jan Samarth Portal (National Portal for Credit-Linked Subsidies)",
        "authority": "Ministry of Finance, Government of India",
        "type": "Credit-Linked Govt Subsidy Platform",
        "eligibility_summary": "Students seeking government-sponsored subsidized education loans.",
        "course_scope": "Graduation, Post-Graduation, Professional courses in India.",
        "benefits": "Instant digital eligibility check, automated matching with suitable government credit schemes, seamless bank routing.",
        "max_loan_eligible": "As per scheme criteria.",
        "income_ceiling": "Depends on individual linked subsidy scheme.",
        "nodal_bank": "All major Public Sector & Scheduled Commercial Banks.",
        "how_to_apply": "Visit www.jansamarth.in -> Select Education Loan category -> Check digital eligibility -> Apply directly.",
        "official_url": "https://www.jansamarth.in",
        "key_notes": [
            "Connects 12+ government credit schemes under one digital umbrella",
            "Provides digital in-principle approval letters from banks",
            "Transparent grievance redressal mechanism"
        ]
    },
    {
        "id": "dr-ambedkar-scheme",
        "name": "Dr. Ambedkar Central Sector Scheme of Interest Subsidy for OBCs and EBCs",
        "authority": "Ministry of Social Justice and Empowerment, Government of India",
        "type": "Overseas Study Interest Subsidy",
        "eligibility_summary": "OBC students with family income <= ₹8 Lakhs p.a. OR Economically Backward Classes (EBC) with income <= ₹5 Lakhs p.a.",
        "course_scope": "Masters, M.Phil, and Ph.D. level courses abroad in designated subjects (Engineering, Science, Tech, Agriculture, Medicine).",
        "benefits": "100% interest subsidy on education loans during moratorium period (course period + 1 year).",
        "max_loan_eligible": "Full interest subsidy on education loan sanctioned by scheduled banks.",
        "income_ceiling": "₹8,00,000 p.a. for OBC; ₹5,00,000 p.a. for EBC.",
        "nodal_bank": "Canara Bank / Scheduled Commercial Banks.",
        "how_to_apply": "Bank submits interest subsidy claim through the Canara Bank portal on behalf of the eligible borrower.",
        "official_url": "https://socialjustice.gov.in/schemes/36",
        "key_notes": [
            "Valid only for overseas higher education at Masters / Ph.D. levels",
            "Applicant must secure admission in accredited foreign universities",
            "Must possess verified Caste / Income certificate from revenue authorities"
        ]
    },
    {
        "id": "cgfsel-guarantee",
        "name": "Credit Guarantee Fund Scheme for Education Loans (CGFSEL)",
        "authority": "National Credit Guarantee Trustee Company (NCGTC)",
        "type": "Collateral-Free Credit Guarantee",
        "eligibility_summary": "Students securing education loan up to ₹7.5 Lakhs without any third-party collateral or guarantee.",
        "course_scope": "All approved higher education courses in India and abroad under IBA Model Scheme.",
        "benefits": "Enables students from non-wealthy backgrounds to get loans up to ₹7.50 Lakhs without pledging house, land, or gold. NCGTC provides 75% credit guarantee to the bank.",
        "max_loan_eligible": "Up to ₹7.5 Lakhs.",
        "income_ceiling": "No income ceiling.",
        "nodal_bank": "All Scheduled Commercial Banks under IBA.",
        "how_to_apply": "Directly requested when applying for education loan up to ₹7.5 Lakhs at any public or scheduled bank.",
        "official_url": "https://www.ncgtc.in/en/cgfsel",
        "key_notes": [
            "Banks CANNOT legally ask for tangible collateral or third-party guarantee for loans up to ₹7.5L under this scheme",
            "Parent / guardian will remain joint co-borrower",
            "Protects meritorious students from being rejected for lack of property assets"
        ]
    },
    {
        "id": "girl-student-rebate",
        "name": "Girl Student Special Interest Rate Concession (0.50% Rebate)",
        "authority": "Indian Banks' Association (IBA) & Leading Public Sector Banks (SBI, BoB, Canara, PNB)",
        "type": "Gender Concession",
        "eligibility_summary": "All female students pursuing higher education.",
        "course_scope": "Both domestic and overseas education loan schemes.",
        "benefits": "Flat 0.50% (50 basis points) discount on card interest rate across the entire loan tenure.",
        "max_loan_eligible": "Applicable across all loan tiers.",
        "income_ceiling": "No income limitation.",
        "nodal_bank": "SBI, Bank of Baroda, Punjab National Bank, Canara Bank, Union Bank of India.",
        "how_to_apply": "Automatically granted upon verifying student gender during application.",
        "official_url": "https://sbi.co.in/web/personal-banking/loans/education-loans",
        "key_notes": [
            "Saves tens of thousands of rupees over a 10 to 15-year repayment tenure",
            "Can be stacked with prompt interest payment discount (e.g. additional 0.5% - 1%)"
        ]
    }
]
