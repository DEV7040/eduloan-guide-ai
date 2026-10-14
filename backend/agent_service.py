"""
EduLoan Guide AI - Agent Service
Implements the full system prompt, responsibilities, strict rules, and hybrid execution
(Gemini API with fallback to built-in knowledge & calculation engine).
"""

import os
import re
import json
from typing import List, Dict, Any, Optional
import httpx

from .loans_db import LOANS_DATABASE, filter_loans
from .schemes_db import SCHEMES_DATABASE
from .calculators import calculate_education_emi, evaluate_eligibility
from .documents_db import generate_document_checklist

SYSTEM_INSTRUCTION = """
You are EduLoan Guide AI, an intelligent assistant that helps students in India find and understand education loans.

Your responsibilities:
1. Loan Finder: Find suitable education loans from banks and government schemes.
2. Eligibility Checker: Assess preliminary eligibility based on course, college, family income, and other relevant criteria.
3. Loan Comparison: Compare interest rates, loan amounts, collateral, fees, and repayment terms.
4. EMI Calculator: Calculate estimated monthly payments, total interest, and repayment costs.
5. Scheme Finder: Identify applicable scholarships, government subsidies, and financial assistance programs.
6. Document Guide: Generate personalized checklists of required documents.
7. Application Assistant: Guide students through the loan application process step by step.
8. Personalized Recommendations: Suggest suitable options based on each student's financial situation and educational goals.
9. Multilingual Support: Explain everything in simple English, Hindi, or Marathi based on the user's preference or input language.
10. Official Sources: Provide verified government and bank links and clearly identify outdated or unverified information.

Rules:
- Never invent interest rates, schemes, or eligibility criteria. Use verified Indian banking facts (SBI, BoB, Canara, PNB, HDFC Credila, CGFSEL, CSIS).
- Never guarantee loan approval. Emphasize that sanctions depend on final credit appraisal and documentation.
- Protect users' personal and financial information.
- Clearly explain assumptions and estimated calculations (e.g. moratorium interest treatment).
- Ask only necessary questions and provide practical next steps.

Official Verified Links:
- Vidya Lakshmi Portal: https://www.vidyalakshmi.co.in
- Jan Samarth Portal: https://www.jansamarth.in
- Central Sector Interest Subsidy (CSIS): https://www.education.gov.in
- SBI Education Loans: https://sbi.co.in/web/personal-banking/loans/education-loans
- Bank of Baroda: https://www.bankofbaroda.in/personal-banking/loans/education-loan
- HDFC Credila: https://www.hdfccredila.com
- Canara Bank: https://canarabank.com
""".strip()

FIRST_MESSAGE_EN = (
    "Hello! Welcome to EduLoan Guide AI 🎓. Are you planning to study in India or abroad? "
    "I'll help you explore suitable education loans, check eligibility, compare options, and estimate your EMI."
)
FIRST_MESSAGE_HI = (
    "नमस्ते! EduLoan Guide AI 🎓 में आपका स्वागत है। क्या आप भारत में पढ़ाई करने की योजना बना रहे हैं या विदेश में? "
    "मैं उपयुक्त एजुकेशन लोन खोजने, पात्रता जांचने, विकल्पों की तुलना करने और अपनी ईएमआई (EMI) का अनुमान लगाने में आपकी मदद करूँगा।"
)
FIRST_MESSAGE_MR = (
    "नमस्कार! EduLoan Guide AI 🎓 मध्ये आपले स्वागत आहे. आपण भारतात शिकण्याचा विचार करत आहात की परदेशात? "
    "मी आपल्याला योग्य शैक्षणिक कर्ज शोधण्यात, पात्रता तपासण्यात, पर्यायांची तुलना करण्यात आणि EMI चा अंदाज लावण्यात मदत करेन."
)


async def call_gemini_api(
    messages: List[Dict[str, str]],
    api_key: str,
    language: str = "en"
) -> Optional[str]:
    """Calls Gemini API using httpx."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

    # Prepare structured context from verified databases
    knowledge_context = (
        "CURRENT VERIFIED KNOWLEDGE BASE:\n"
        f"Available Loans: {json.dumps(LOANS_DATABASE, indent=2)}\n"
        f"Available Schemes: {json.dumps(SCHEMES_DATABASE, indent=2)}\n"
    )

    contents = []
    # Add system context in the first user turn or system instruction
    for msg in messages:
        role = "user" if msg["role"] == "user" else "model"
        contents.append({
            "role": role,
            "parts": [{"text": msg["content"]}]
        })

    payload = {
        "system_instruction": {
            "parts": [{
                "text": (
                    f"{SYSTEM_INSTRUCTION}\n\n"
                    f"Selected language preference: {language}.\n"
                    f"{knowledge_context}"
                )
            }]
        },
        "contents": contents,
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": 2048,
        }
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "")
            else:
                print(f"Gemini API returned error {resp.status_code}: {resp.text}")
    except Exception as e:
        print(f"Exception during Gemini API call: {e}")

    return None


def extract_numbers_from_text(text: str) -> Dict[str, Any]:
    """Helper to detect numbers for loan amount and tenure from user input."""
    # Look for lakh / cr mentions
    lakh_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:lakh|lakhs|lac|lacs|l)', text, re.IGNORECASE)
    cr_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:crore|crores|cr)', text, re.IGNORECASE)
    raw_number = re.search(r'(?:₹|rs\.?|inr)?\s*([1-9]\d{4,9})', text, re.IGNORECASE)

    amount = None
    if lakh_match:
        amount = float(lakh_match.group(1)) * 100000
    elif cr_match:
        amount = float(cr_match.group(1)) * 10000000
    elif raw_number:
        amount = float(raw_number.group(1))

    return {"amount": amount}


def rule_based_expert_agent(
    messages: List[Dict[str, str]],
    language: str = "en"
) -> str:
    """
    Intelligent built-in conversational AI with domain expertise in Indian education loans.
    Handles English, Hindi, and Marathi with verified facts, calculators, schemes, and links.
    """
    if not messages:
        if language == "hi":
            return FIRST_MESSAGE_HI
        elif language == "mr":
            return FIRST_MESSAGE_MR
        return FIRST_MESSAGE_EN

    last_user_msg = messages[-1]["content"].strip().lower()

    # Detect language from input if not set explicitly
    is_hi = language == "hi" or any(w in last_user_msg for w in ["नमस्ते", "ऋण", "लोन", "ब्याज", "विदेश", "भारत", "पात्रता"])
    is_mr = language == "mr" or any(w in last_user_msg for w in ["नमस्कार", "कर्ज", "परदेश", "भारतात", "कागदपत्रे"])

    # 1. Greetings
    if re.search(r'^(hi|hello|hey|namaste|greetings|start|kem cho|ram ram)', last_user_msg):
        if is_hi:
            return FIRST_MESSAGE_HI
        elif is_mr:
            return FIRST_MESSAGE_MR
        return FIRST_MESSAGE_EN

    # 2. Check for EMI calculation queries
    if any(k in last_user_msg for k in ["emi", "calculate", "monthly payment", "हफ्ता", "ईएमआई", "गणना"]):
        num_info = extract_numbers_from_text(last_user_msg)
        amount = num_info["amount"] or 1500000
        tenure = 10
        rate = 9.5
        calc = calculate_education_emi(amount, rate, tenure, moratorium_years=2.0)

        if is_hi:
            return (
                f"### 🧮 अनुमानित ईएमआई (EMI) गणना\n\n"
                f"- **लोन राशि:** ₹{amount:,.0f}\n"
                f"- **अनुमानित ब्याज दर:** {rate}% प्रति वर्ष (फ्लोटिंग/EBLR)\n"
                f"- **भुगतान अवधि (Tenure):** {tenure} वर्ष ({tenure*12} महीने)\n"
                f"- **मोराटोरियम अवधि (कोर्स):** 2 वर्ष\n"
                f"- **अनुमानित मासिक ईएमआई:** **₹{calc['monthly_emi']:,.0f} / माह**\n"
                f"- **कुल देय ब्याज:** ₹{calc['total_interest_paid']:,.0f}\n"
                f"- **कुल भुगतान राशि:** ₹{calc['total_amount_payable']:,.0f}\n\n"
                f"> **नोट:** यदि आप पढ़ाई के दौरान साधारण ब्याज का भुगतान करते हैं, तो बैंक आमतौर पर **1.00% की छूट** देते हैं! इसके अलावा छात्रा (Girl Student) होने पर **0.50% की अतिरिक्त छूट** मिलती है।\n\n"
                f"क्या आप विभिन्न बैंकों (जैसे SBI, BoB, HDFC Credila) की दरों की तुलना करना चाहते हैं?"
            )
        elif is_mr:
            return (
                f"### 🧮 अंदाजित ईएमआय (EMI) हिशोब\n\n"
                f"- **कर्जाची रक्कम:** ₹{amount:,.0f}\n"
                f"- **व्याजदर:** {rate}% प्रति वर्ष\n"
                f"- **परतफेड कालावधी:** {tenure} वर्षे\n"
                f"- **अंदाजित मासिक हप्ता (EMI):** **₹{calc['monthly_emi']:,.0f} / महिना**\n"
                f"- **एकूण व्याज:** ₹{calc['total_interest_paid']:,.0f}\n"
                f"- **एकूण परतफेड रक्कम:** ₹{calc['total_amount_payable']:,.0f}\n\n"
                f"> **महत्त्वाचे:** मोराटोरियम कालावधीत व्याज भरल्यास बँका **1% सवलत** देतात आणि विद्यार्थिनींसाठी **0.50% अतिरिक्त सवलत** लागू होते.\n\n"
                f"आपण पात्रता तपासू इच्छिता की इतर बँकांची तुलना करू इच्छिता?"
            )
        else:
            return (
                f"### 🧮 Estimated Education Loan EMI Calculation\n\n"
                f"- **Principal Amount:** ₹{amount:,.0f}\n"
                f"- **Indicative Interest Rate:** {rate}% p.a. (Floating / EBLR linked)\n"
                f"- **Repayment Tenure:** {tenure} years ({tenure*12} months)\n"
                f"- **Moratorium Period (Study duration):** 2 years (capitalized simple interest)\n"
                f"- **Estimated Monthly EMI:** **₹{calc['monthly_emi']:,.0f} / month**\n"
                f"- **Total Interest Payable:** ₹{calc['total_interest_paid']:,.0f}\n"
                f"- **Total Repayment Amount:** ₹{calc['total_amount_payable']:,.0f}\n\n"
                f"> **Key Tips:**\n"
                f"> - **Prompt Interest Service:** Paying simple interest during the course period saves approx **₹{calc['estimated_savings_with_prompt_service']:,.0f}** over the tenure!\n"
                f"> - **Girl Student Concession:** Female students get an automatic **0.50% interest rate rebate** at public sector banks (SBI, BoB, Canara, PNB).\n"
                f"> - **Tax Benefit:** Interest paid is 100% tax-deductible under **Section 80E** of the Income Tax Act for up to 8 years.\n\n"
                f"Would you like to customize this with your exact loan amount, or compare SBI vs HDFC Credila rates?"
            )

    # 3. Documents query
    if any(k in last_user_msg for k in ["document", "docs", "paperwork", "checklist", "कागदपत्र", "दस्तावेज", "डॉक्यूमेंट"]):
        dest = "abroad" if any(w in last_user_msg for w in ["abroad", "foreign", "विदेश", "परदेश"]) else "india"
        if is_hi:
            return (
                f"### 📑 एजुकेशन लोन के लिए आवश्यक दस्तावेज़ चेकलिस्ट ({dest.upper()})\n\n"
                f"**1. छात्र/छात्रा के दस्तावेज़:**\n"
                f"- आधार कार्ड, पैन कार्ड (अनिवार्य) और पासपोर्ट फोटो\n"
                f"- 10वीं, 12वीं और स्नातक (Graduation) की मार्कशीट और डिग्री\n"
                f"- प्रवेश परीक्षा स्कोरकार्ड (JEE / NEET / CAT / GRE / IELTS / TOEFL)\n"
                f"- कॉलेज का ऑफर लेटर और फीस स्ट्रक्चर\n\n"
                f"**2. सह-आवेदक (माता-पिता / अभिभावक) के वित्तीय दस्तावेज़:**\n"
                f"- पैन और आधार कार्ड\n"
                f"- पिछले 6 महीने का बैंक स्टेटमेंट (वेतन खाता या चालू खाता)\n"
                f"- नौकरीपेशा: पिछले 3 महीने की सैलरी स्लिप और 2 साल का Form 16 / ITR\n"
                f"- व्यवसायी: पिछले 2-3 साल का ITR और बैलेंस शीट\n\n"
                f"**3. जमानत / संपार्श्विक (Collateral) दस्तावेज़ (यदि लोन ₹7.5 लाख से अधिक है):**\n"
                f"- रजिस्टर्ड सेल डीड / टाइटल डीड और 30 साल की चैन डीड\n"
                f"- नॉन-एन्कम्ब्रन्स सर्टिफिकेट (NEC) और म्यूनिसिपल टैक्स रसीद\n\n"
                f"> **नोट:** ₹7.5 लाख तक के लोन के लिए **CGFSEL गारंटी** के तहत किसी भी संपत्ति (Collateral) की आवश्यकता नहीं होती!\n\n"
                f"क्या आप विद्या लक्ष्मी पोर्टल ([www.vidyalakshmi.co.in](https://www.vidyalakshmi.co.in)) पर आवेदन की प्रक्रिया समझना चाहते हैं?"
            )
        elif is_mr:
            return (
                f"### 📑 शैक्षणिक कर्जासाठी आवश्यक कागदपत्रे ({dest.upper()})\n\n"
                f"**1. विद्यार्थ्याची कागदपत्रे:**\n"
                f"- आधार कार्ड, पॅन कार्ड आणि पासपोर्ट आकाराचे फोटो\n"
                f"- 10वी, 12वी आणि पदवीच्या सर्व गुणपत्रिका (Marksheets)\n"
                f"- प्रवेश परीक्षा निकाल (CET/JEE/GRE/IELTS)\n"
                f"- महाविद्यालयाचे प्रवेश पत्र (Admit letter) आणि फी चे विवरण\n\n"
                f"**2. सह-कर्जदार (पालक) कागदपत्रे:**\n"
                f"- पॅन कार्ड, आधार कार्ड\n"
                f"- मागील 6 महिन्यांचे बँक स्टेटमेंट\n"
                f"- नोकरदारांसाठी 3 महिन्यांच्या सॅलरी स्लिप्स आणि 2 वर्षांचे Form 16/ITR\n"
                f"- व्यवसायिकांसाठी मागील 3 वर्षांचे ITR\n\n"
                f"**3. तारण (Collateral) कागदपत्रे (₹7.5 लाखांपेक्षा जास्त असल्यास):**\n"
                f"- जागेचे / घराचे खरेदीखत (Sale Deed), 7/12 उतारा किंवा बोजा नसलेला दाखला (NEC)\n\n"
                f"> **नियम:** ₹7.5 लाखांपर्यंत **CGFSEL** अंतर्गत कोणतेही तारण लागत नाही.\n\n"
                f"आपण अधिक माहितीसाठी विद्या लक्ष्मी पोर्टलवर ([www.vidyalakshmi.co.in](https://www.vidyalakshmi.co.in)) अर्ज करू शकता."
            )
        else:
            return (
                f"### 📑 Personalized Education Loan Document Checklist ({dest.upper()})\n\n"
                f"Here are the mandatory documents requested by public and private lenders in India:\n\n"
                f"**1. Student / Applicant Documents:**\n"
                f"- **KYC:** PAN Card & Aadhaar Card (mandatory), Passport copy (mandatory for abroad).\n"
                f"- **Academic Record:** 10th, 12th, and Degree marksheets & passing certificates.\n"
                f"- **Entrance & Test Scores:** JEE / CAT / GATE or abroad test scores (GRE / GMAT / IELTS / TOEFL).\n"
                f"- **Admission Proof:** Official unconditional admission offer letter + university fee schedule.\n\n"
                f"**2. Co-Applicant (Parents / Guardian / Spouse) Financial Documents:**\n"
                f"- KYC (PAN Card & Aadhaar Card).\n"
                f"- **Bank Statement:** Last 6 months bank statement showing regular salary credit or business turnover.\n"
                f"- **Income Proof (Salaried):** Latest 3 months salary slips + 2 years Form 16 & ITR acknowledgments.\n"
                f"- **Income Proof (Self-Employed / Business):** 2-3 years audited P&L, balance sheets, and ITR computations.\n\n"
                f"**3. Collateral Documents (Only required if loan exceeds ₹7.5 Lakhs):**\n"
                f"- Title Deed / Registered Sale deed of immovable property (house, flat, non-agricultural land).\n"
                f"- 30-year Chain deeds and Non-Encumbrance Certificate (NEC).\n"
                f"- Alternatively: Bank Fixed Deposit (FD) or LIC Surrender Value receipts.\n\n"
                f"> **Important Rule:** Under the Government's **CGFSEL** framework, banks cannot ask for tangible collateral or third-party guarantee for loans **up to ₹7.5 Lakhs**.\n\n"
                f"Use our **Document Checklist tab** above to generate and tick off your personalized checklist!"
            )

    # 4. Schemes & Subsidies query (CSIS, Vidya Lakshmi, JanSamarth, etc.)
    if any(k in last_user_msg for k in ["scheme", "subsidy", "csis", "scholarship", "vidya lakshmi", "jansamarth", "योजना", "सब्सिडी", "सवलत"]):
        if is_hi:
            return (
                f"### 🏛️ प्रमुख सरकारी योजनाएँ और ब्याज सब्सिडी (Government Schemes)\n\n"
                f"1. **केंद्रीय क्षेत्र ब्याज सब्सिडी योजना (CSIS):**\n"
                f"   - **लाभ:** पढ़ाई और मोराटोरियम अवधि (कोर्स + 1 वर्ष) के दौरान **100% ब्याज सरकार देती है**।\n"
                f"   - **पात्रता:** वार्षिक पारिवारिक आय ₹4.50 लाख तक (EWS प्रमाण पत्र आवश्यक)। केवल भारत में तकनीकी/व्यावसायिक पाठ्यक्रमों के लिए मान्य।\n"
                f"   - **नोडल बैंक:** केनरा बैंक ([Canara Bank](https://canarabank.com))\n\n"
                f"2. **पीएम विद्या लक्ष्मी पोर्टल (Vidya Lakshmi):**\n"
                f"   - वित्त मंत्रालय द्वारा संचालित सिंगल-विंडो पोर्टल ([www.vidyalakshmi.co.in](https://www.vidyalakshmi.co.in))।\n"
                f"   - एक सामान्य फॉर्म (CELAF) भरकर आप एक साथ 3 बैंकों में आवेदन कर सकते हैं।\n\n"
                f"3. **जन समर्थ पोर्टल (Jan Samarth):**\n"
                f"   - क्रेडिट लिंक्ड सरकारी योजनाओं के लिए डिजिटल पोर्टल ([www.jansamarth.in](https://www.jansamarth.in))।\n"
                f"   - त्वरित डिजिटल इन-प्रिंसिपल अप्रूवल प्रदान करता है।\n\n"
                f"4. **डॉ. आंबेडकर योजना (OBC/EBC छात्रों के लिए विदेश अध्ययन):**\n"
                f"   - मास्टर/पीएचडी स्तर की पढ़ाई के लिए मोराटोरियम अवधि का पूरा ब्याज सब्सिडी में माफ होता है।\n\n"
                f"5. **छात्राओं के लिए 0.50% की ब्याज छूट:**\n"
                f"   - SBI, बैंक ऑफ बड़ौदा, PNB और केनरा बैंक में सभी महिला छात्रों को ब्याज में सीधी छूट मिलती है।\n\n"
                f"क्या आपकी पारिवारिक वार्षिक आय ₹4.5 लाख से कम है ताकि CSIS सब्सिडी की जांच की जा सके?"
            )
        elif is_mr:
            return (
                f"### 🏛️ प्रमुख सरकारी योजना आणि व्याज सवलत (Govt Schemes)\n\n"
                f"1. **CSIS केंद्रीय व्याज सवलत योजना:**\n"
                f"   - **फायदा:** शिक्षण कालावधीत (मोराटोरियम) **100% व्याज सरकार भरते**.\n"
                f"   - **पात्रता:** कौटुंबिक वार्षिक उत्पन्न ₹4.5 लाखांपेक्षा कमी असणाऱ्या EWS विद्यार्थ्यांसाठी (भारतातील व्यावसायिक शिक्षणासाठी).\n\n"
                f"2. **विद्या लक्ष्मी पोर्टल (Vidya Lakshmi):**\n"
                f"   - केंद्र सरकारचे अधिकृत पोर्टल: [www.vidyalakshmi.co.in](https://www.vidyalakshmi.co.in)\n"
                f"   - एकाच अर्जावरून (CELAF) 3 वेगवेगळ्या बँकांमध्ये अर्ज करता येतो.\n\n"
                f"3. **मुलींसाठी 0.50% व्याज सवलत:**\n"
                f"   - सर्व सरकारी बँकांमध्ये विद्यार्थिनींसाठी व्याजात विशेष सूट दिली जाते.\n\n"
                f"आपण कोणत्या अभ्यासक्रमासाठी आणि कोणत्या देशात शिकू इच्छिता?"
            )
        else:
            return (
                f"### 🏛️ Verified Government Subsidies & Educational Loan Schemes\n\n"
                f"Here are the primary verified central schemes you should know about:\n\n"
                f"1. **Central Sector Interest Subsidy Scheme (CSIS):**\n"
                f"   - **Authority:** Ministry of Education, Government of India.\n"
                f"   - **Benefit:** **100% Interest waiver** during the study period and moratorium (Course + 1 year). The Government pays the interest directly to the bank.\n"
                f"   - **Eligibility:** Gross parental annual income **≤ ₹4.50 Lakhs**; pursuing recognized professional/technical courses in India.\n"
                f"   - **Nodal Agency:** [Canara Bank](https://canarabank.com).\n\n"
                f"2. **Vidya Lakshmi Portal (CELAF):**\n"
                f"   - **Official Portal:** [www.vidyalakshmi.co.in](https://www.vidyalakshmi.co.in)\n"
                f"   - Developed under Ministry of Finance & IBA. Single electronic window to apply to 3 banks simultaneously with one Common Education Loan Application Form.\n\n"
                f"3. **Jan Samarth Portal:**\n"
                f"   - **Official Portal:** [www.jansamarth.in](https://www.jansamarth.in)\n"
                f"   - Government's one-stop portal for credit-linked subsidies, providing digital in-principle sanction.\n\n"
                f"4. **Credit Guarantee Fund (CGFSEL):**\n"
                f"   - **Benefit:** Mandates that loans up to **₹7.5 Lakhs** require **zero collateral and zero third-party guarantee**.\n\n"
                f"5. **Girl Student Concession:**\n"
                f"   - **SBI, Bank of Baroda, PNB, and Canara Bank** provide an automatic **0.50% interest concession** across the entire loan repayment lifespan.\n\n"
                f"Does your family income fall within the ₹4.5 Lakhs threshold to claim the CSIS subsidy?"
            )

    # 5. Loan Finder / Comparison query
    if any(k in last_user_msg for k in ["compare", "bank", "rate", "sbi", "hdfc", "credila", "baroda", "pnb", "तुलना", "बँक", "व्याज"]):
        if is_hi:
            return (
                f"### ⚖️ प्रमुख बैंकों की एजुकेशन लोन तुलना\n\n"
                f"| बैंक / संस्थान | ब्याज दर (वार्षिक) | अधिकतम राशि | बिना जमानत (Collateral-Free) सीमा | मार्जिन मनी |\n"
                f"| :--- | :--- | :--- | :--- | :--- |\n"
                f"| **SBI (State Bank of India)** | 8.15% - 10.15% | भारत: ₹50L / विदेश: ₹1.5 Cr | ₹7.5L (IIT/IIM के लिए ₹40L तक) | भारत: 5% / विदेश: 15% |\n"
                f"| **Bank of Baroda** | 8.10% - 9.90% | विदेश: ₹80L / भारत: ₹40L | ₹7.5L (शीर्ष संस्थानों के लिए ₹40L) | भारत: 0% / विदेश: 10% |\n"
                f"| **PNB (Punjab National Bank)** | 8.55% - 10.45% | ₹1.0 Crore | ₹7.5 Lakhs | भारत: 5% / विदेश: 15% |\n"
                f"| **HDFC Credila (NBFC)** | 9.50% - 13.25% | ₹2.0 Crores तक | ₹40-50 Lakhs (प्रोफाइल आधार पर) | 0% - 100% फंडिंग |\n\n"
                f"💡 **सलाह:**\n"
                f"- **पब्लिक बैंक (SBI / BoB):** सबसे कम ब्याज दरें और सरकारी सब्सिडी (CSIS) का पूरा लाभ।\n"
                f"- **प्राइवेट / NBFC (HDFC Credila / Avanse):** बिना प्रॉपर्टी गिरवी रखे ₹40-50 लाख तक तेजी से लोन (वीजा से पहले अप्रूवल)।\n\n"
                f"आपकी पढ़ाई का स्थान और अपेक्षित लोन राशि क्या है?"
            )
        elif is_mr:
            return (
                f"### ⚖️ प्रमुख बँकांच्या शैक्षणिक कर्जांची तुलना\n\n"
                f"| बँक | अंदाजित व्याजदर | कमाल मर्यादा | विना-तारण (Collateral-Free) मर्यादा |\n"
                f"| :--- | :--- | :--- | :--- |\n"
                f"| **SBI** | 8.15% - 10.15% | ₹50L (भारत) / ₹1.5 Cr (परदेश) | ₹7.5 लाख (प्रीमियर कॉलेजसाठी ₹40 लाख) |\n"
                f"| **Bank of Baroda** | 8.10% - 9.90% | ₹80 लाख | ₹7.5 लाख (शीर्ष कॉलेजसाठी ₹40 लाख) |\n"
                f"| **HDFC Credila** | 9.50% - 13.25% | ₹2 कोटीपर्यंत | ₹40-50 लाख (अनसिक्युअर्ड) |\n\n"
                f"आपण कोणत्या बँकेत अर्ज करू इच्छिता? आपण थेट [Vidya Lakshmi Portal](https://www.vidyalakshmi.co.in) वरून अर्ज करू शकता."
            )
        else:
            return (
                f"### ⚖️ Top Education Loan Comparison (Public Banks vs Private/NBFCs)\n\n"
                f"| Lender | Indicative Rate (p.a.) | Max Loan Amount | Collateral-Free Limit | Margin Money |\n"
                f"| :--- | :--- | :--- | :--- | :--- |\n"
                f"| **State Bank of India (SBI)** | 8.15% – 10.15% | India: ₹50L / Abroad: ₹1.5 Cr | Up to ₹7.5L (₹40L for IIT/IIM List AA) | 5% (India > ₹4L), 15% (Abroad) |\n"
                f"| **Bank of Baroda (BoB)** | 8.10% – 9.90% | Abroad: ₹80L / India: ₹40L | Up to ₹7.5L (₹40L for top global/India univs) | Nil for premier, 10% abroad |\n"
                f"| **Punjab National Bank (PNB)** | 8.55% – 10.45% | Up to ₹1.0 Crore | Up to ₹7.5 Lakhs | 15% for overseas |\n"
                f"| **HDFC Credila (Specialized)**| 9.50% – 13.25% | Up to ₹2.0 Crores | Up to ₹45-50 Lakhs (Unsecured based on profile) | 0% (Up to 100% cost funded) |\n"
                f"| **Avanse Financial Services** | 10.25% – 14.50% | Up to ₹1.5 Crores | Up to ₹50 Lakhs unsecured | Nil margin money |\n\n"
                f"> **Strategic Recommendation:**\n"
                f"> - **Choose Public Banks (SBI / BoB):** If you or a co-applicant have property collateral or are attending a Tier-1 college, you will save lakhs due to 1.5% to 3.0% lower interest rates.\n"
                f"> - **Choose NBFCs (HDFC Credila / Avanse):** If you are studying abroad and need ₹30L - ₹50L **without pledging immovable property**, or need sanction before visa interview.\n\n"
                f"Would you like to calculate the exact monthly EMI for any of these options?"
            )

    # 6. Destination specific (India vs Abroad response)
    if "abroad" in last_user_msg or "विदेश" in last_user_msg or "परदेश" in last_user_msg:
        if is_hi:
            return (
                f"### 🌍 विदेश में पढ़ाई (Study Abroad) के लिए एजुकेशन लोन गाइड\n\n"
                f"विदेश में पढ़ाई के लिए भारतीय बैंक मुख्य रूप से दो प्रकार के लोन देते हैं:\n\n"
                f"1. **सुरक्षित लोन (Secured Loan - SBI Global Ed-vantage / BoB Scholar):**\n"
                f"   - **ब्याज दर:** ~8.65% से 10.15%\n"
                f"   - **जमानत (Collateral):** आवासीय फ्लैट, मकान या बैंक एफडी आवश्यक।\n"
                f"   - **मार्जिन मनी:** लगभग 15%\n"
                f"   - **अधिकतम लोन:** ₹1.5 करोड़ तक।\n\n"
                f"2. **असुरक्षित लोन (Unsecured Loan - HDFC Credila / Avanse / ICICI):**\n"
                f"   - **ब्याज दर:** ~9.50% से 13.50%\n"
                f"   - **जमानत:** कोई प्रॉपर्टी गिरवी रखने की जरूरत नहीं (₹40-50 लाख तक)।\n"
                f"   - **वीजा से पहले अप्रूवल:** I-20 / CAS लेटर के आधार पर त्वरित स्वीकृति।\n\n"
                f"आप किस देश (उदा. USA, UK, Canada, Germany) में किस कोर्स के लिए जा रहे हैं, और अपेक्षित खर्च कितना है?"
            )
        elif is_mr:
            return (
                f"### 🌍 परदेशात शिक्षणासाठी (Study Abroad) कर्ज मार्गदर्शक\n\n"
                f"1. **सरकारी बँका (SBI / Bank of Baroda):**\n"
                f"   - कमी व्याजदर (8.65% - 9.90%), तारण (घर/जमीन) आवश्यक.\n"
                f"2. **NBFCs (HDFC Credila / Avanse):**\n"
                f"   - ₹40-50 लाखांपर्यंत विना-तारण (Unsecured) कर्ज उपलब्ध, जलद मंजुरी.\n\n"
                f"आपण कोणत्या देशात कोणत्या अभ्यासक्रमासाठी जात आहात?"
            )
        else:
            return (
                f"### 🌍 Overseas Education Loan Guide (Studying Abroad)\n\n"
                f"When planning to study abroad (USA, UK, Canada, Germany, Australia, Ireland), Indian lenders offer two main pathways:\n\n"
                f"1. **Secured Education Loans (Public Banks - SBI Global Ed-vantage / BoB Scholar):**\n"
                f"   - **Interest Rates:** 8.65% to 10.15% (Lowest cost)\n"
                f"   - **Collateral:** Residential property, commercial plot, or Fixed Deposit required for > ₹7.5 Lakhs.\n"
                f"   - **Loan Amount:** Up to ₹1.5 Crores.\n"
                f"   - **Margin Money:** Typically 15% (Scholarships can be counted towards margin).\n\n"
                f"2. **Unsecured Education Loans (NBFCs & Private Banks - HDFC Credila / Avanse / Axis):**\n"
                f"   - **Interest Rates:** 9.50% to 13.50%\n"
                f"   - **Collateral:** No property mortgage required up to ₹40 Lakhs - ₹50 Lakhs based on test scores (GRE/GMAT) and university ranking.\n"
                f"   - **Speed:** Faster processing (3-7 days) with pre-visa sanction letters.\n\n"
                f"Which country and degree are you targeting, and what is your approximate loan requirement?"
            )

    if "india" in last_user_msg or "भारत" in last_user_msg:
        if is_hi:
            return (
                f"### 🇮🇳 भारत में पढ़ाई के लिए एजुकेशन लोन गाइड\n\n"
                f"भारत में उच्च शिक्षा (B.Tech, MBA, MBBS, Law, etc.) के लिए मुख्य नियम:\n\n"
                f"1. **₹4 लाख तक:** 0% मार्जिन मनी, कोई जमानत नहीं।\n"
                f"2. **₹4 लाख से ₹7.5 लाख:** केवल 5% मार्जिन मनी, **CGFSEL गारंटी के तहत कोई संपत्ति गिरवी रखने की आवश्यकता नहीं**।\n"
                f"3. **आईआईटी / आईआईएम (IIT / IIM) छात्र:** SBI Scholar Loan के तहत ₹40 लाख तक 100% बिना किसी जमानत के उपलब्ध।\n"
                f"4. **सरकारी CSIS ब्याज सब्सिडी:** यदि पारिवारिक आय ₹4.5 लाख से कम है, तो पढ़ाई के दौरान का पूरा ब्याज भारत सरकार भरेगी।\n\n"
                f"आवेदन करने के लिए आप सीधे [Vidya Lakshmi Portal](https://www.vidyalakshmi.co.in) पर रजिस्टर कर सकते हैं।\n\n"
                f"आप किस कॉलेज/कोर्स में प्रवेश ले रहे हैं?"
            )
        else:
            return (
                f"### 🇮🇳 Domestic Education Loan Guide (Studying in India)\n\n"
                f"Under the Indian Banks' Association (IBA) Model Scheme for studies in India:\n\n"
                f"1. **Up to ₹4.0 Lakhs:** Zero margin money requirement, zero collateral.\n"
                f"2. **₹4.0 Lakhs to ₹7.5 Lakhs:** Only 5% margin money. Fully covered by the **CGFSEL Government Guarantee** — no tangible collateral or third-party guarantor permitted to be demanded by banks.\n"
                f"3. **Premier Institutions (IITs, IIMs, NITs, AIIMS, XLRI):** Special schemes like **SBI Scholar Loan** and **Baroda Scholar** offer up to **₹40 Lakhs collateral-free** at rock-bottom interest rates (~8.0% - 8.5%).\n"
                f"4. **CSIS Interest Subsidy:** If your annual household income is under ₹4.50 Lakhs, the Government pays **100% of the moratorium interest** on professional & technical courses.\n\n"
                f"Which course and university are you enrolling in?"
            )

    # Default informative walkthrough
    if is_hi:
        return (
            f"मैं **EduLoan Guide AI** हूँ 🎓। मैं आपकी निम्नलिखित में सहायता कर सकता हूँ:\n\n"
            f"1. **ईएमआई कैलकुलेटर:** अपनी लोन राशि और अवधि के अनुसार ईएमआई और मोराटोरियम ब्याज जानें।\n"
            f"2. **पात्रता जांच:** अपने कॉलेज, आय और सिबिल स्कोर के आधार पर बैंक स्वीकृति की संभावना देखें।\n"
            f"3. **बैंक तुलना:** SBI, BoB, PNB, HDFC Credila और Avanse की ब्याज दरों और शर्तों की तुलना।\n"
            f"4. **सरकारी योजनाएं:** CSIS ब्याज सब्सिडी, विद्या लक्ष्मी पोर्टल और छात्राओं के लिए 0.5% छूट।\n"
            f"5. **दस्तावेज़ सूची:** लोन के लिए आवश्यक कागजी कार्रवाई की व्यक्तिगत चेकलिस्ट।\n\n"
            f"कृपया बताएं: आप भारत में पढ़ाई करने वाले हैं या विदेश में, और आपको लगभग कितनी राशि की आवश्यकता है?"
        )
    elif is_mr:
        return (
            f"मी **EduLoan Guide AI** आहे 🎓. मी आपल्याला खालील बाबींमध्ये मदत करू शकतो:\n\n"
            f"1. **EMI कॅल्क्युलेटर:** आपल्या कर्जाच्या हप्त्याची आणि व्याजाची अचूक माहिती.\n"
            f"2. **पात्रता तपासणी:** उत्पन्न, महाविद्यालय आणि CIBIL स्कोअरनुसार कर्जाची शक्यता.\n"
            f"3. **बँकांची तुलना:** SBI, BoB, HDFC Credila चे व्याजदर आणि अटी.\n"
            f"4. **सरकारी योजना:** CSIS व्याज सवलत, विद्या लक्ष्मी पोर्टल.\n"
            f"5. **कागदपत्रे चेकलिस्ट:** आवश्यक कागदपत्रांची संपूर्ण यादी.\n\n"
            f"आपण भारतात शिक्षण घेत आहात की परदेशात?"
        )
    else:
        return (
            f"I am **EduLoan Guide AI** 🎓, your verified guide for Indian education financing.\n\n"
            f"Here is what I can assist you with right now:\n\n"
            f"1. **EMI & Repayment Calculator:** Calculate your monthly outflow with moratorium interest capitalization.\n"
            f"2. **Eligibility Evaluator:** Check your loan approval probability based on university tier, CIBIL score, and income.\n"
            f"3. **Bank Comparison:** Compare SBI, Bank of Baroda, PNB, Canara, and HDFC Credila rates side by side.\n"
            f"4. **Government Subsidies:** Claim the Central Sector Interest Subsidy (CSIS) or girl student interest rebate.\n"
            f"5. **Document Checklist:** Generate your personalized KYC, academic, co-applicant, and collateral requirements.\n\n"
            f"To get started: Are you planning to study in India or abroad, and what is your approximate loan requirement?"
        )


async def generate_agent_response(
    messages: List[Dict[str, str]],
    api_key: Optional[str] = None,
    language: str = "en"
) -> str:
    """Hybrid orchestrator: attempts Gemini API call if key is present; falls back seamlessly to domain rule engine."""
    # Look for API key from request, or environment
    active_key = api_key or os.environ.get("GEMINI_API_KEY", "").strip()

    if active_key:
        try:
            llm_response = await call_gemini_api(messages, active_key, language=language)
            if llm_response and len(llm_response.strip()) > 10:
                return llm_response
        except Exception as e:
            print(f"Fallback to rule-based engine due to: {e}")

    # Fallback to expert domain engine
    return rule_based_expert_agent(messages, language=language)
