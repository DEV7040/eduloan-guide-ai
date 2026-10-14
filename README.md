# EduLoan Guide AI 🎓

> **India's Intelligent Education Loan & Government Scheme Assistant**  
> Compliant with standard Reserve Bank of India (RBI) and Indian Banks' Association (IBA) Model Education Loan Scheme guidelines.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=flat&logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-8.0-646CFF?style=flat&logo=vite&logoColor=white)](https://vitejs.dev/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## 🌟 Overview

**EduLoan Guide AI** is an end-to-end intelligent assistant built to simplify higher education financing for Indian students pursuing studies domestically or abroad. It replaces confusing bank circulars and hidden loan terms with an interactive, transparent suite of tools:

1. **Loan Finder:** Search and filter verified education loan products from top public banks (SBI, BoB, PNB, Canara), private banks (Axis, ICICI), and specialized NBFCs (HDFC Credila, Avanse).
2. **Eligibility Checker:** Instant preliminary eligibility scoring based on course tier (IIT/IIM/NIT List AA/A), family income, co-applicant CIBIL score, and collateral availability.
3. **Loan Comparison Matrix:** Side-by-side comparison of interest rates, collateral requirements, margin money, and moratorium terms.
4. **EMI & Moratorium Calculator:** Calculates monthly outflow, simple interest accrual during the moratorium (study + grace period), and interest capitalization.
5. **Scheme Finder:** Automatically matches eligible students to central subsidies such as the **Central Sector Interest Subsidy (CSIS)**, **Credit Guarantee Fund Scheme for Education Loans (CGFSEL)**, and girl child interest concessions.
6. **Personalized Document Guide:** Dynamic checklist generator tailored to study destination (India vs Abroad) and co-applicant profession (Salaried, Self-Employed, Farmer/Agriculturist).
7. **Application Roadmap:** Direct integration instructions for the **Vidya Lakshmi Portal (CELAF)** and **Jan Samarth Portal**.
8. **Multilingual Support:** Conversational guidance in **English**, **Hindi (हिंदी)**, and **Marathi (मराठी)**.
9. **Official Verified Sources:** Links directly to authentic government and banking portals with no third-party ads or unverified claims.
10. **Strict Rules:** Never hallucinates interest rates, never makes false approval guarantees, and ensures complete client privacy.

---

## 🏗️ Architecture

EduLoan Guide AI utilizes a **Hybrid AI Architecture**:
- **Built-in Knowledge Engine (Default):** Functions 100% offline with verified Indian banking facts, IBA model scheme rules, and financial amortization algorithms.
- **Google Gemini API (Enhanced):** Seamlessly upgrades to multi-turn conversational reasoning when an optional Gemini API key is provided via UI settings or `.env`.

```
eduloan-guide-ai/
├── backend/
│   ├── main.py             # FastAPI REST endpoints + Single Page Application server
│   ├── agent_service.py    # Hybrid agent orchestrator (Gemini API + Rule Engine)
│   ├── calculators.py      # Education loan EMI, moratorium capitalization & eligibility math
│   ├── loans_db.py         # Verified Indian banks & NBFC loan database
│   ├── schemes_db.py       # Government subsidies & official portals database
│   └── documents_db.py     # Categorized document checklist generator
├── frontend/
│   ├── src/
│   │   ├── components/     # Chat, Calculator, Eligibility, Comparison, Schemes, Documents
│   │   ├── api.js          # REST client
│   │   ├── App.jsx         # Dashboard shell & language selector
│   │   └── index.css       # Responsive design system
│   ├── package.json
│   └── vite.config.js
├── demo_agent.py           # Console demonstration runner
├── test_suite_all.py       # Comprehensive 20-test automated validation suite
└── requirements.txt        # Python dependencies
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- **Python 3.10+**
- **Node.js 18+** & npm

### 2. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/<your-username>/eduloan-guide-ai.git
cd eduloan-guide-ai

# Install backend dependencies
pip install -r requirements.txt

# Install frontend dependencies and build
cd frontend
npm install
npm run build
cd ..
```

### 3. Run the Full-Stack Web Application

```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8080
```
Open your browser at **[http://127.0.0.1:8080](http://127.0.0.1:8080)**.

---

## 🧪 Testing

Run the automated test suite covering all 10 core responsibilities, financial math, and compliance rules:

```bash
python test_suite_all.py
```

Run the interactive terminal showcase:

```bash
python demo_agent.py
```

---

## 🏛️ Verified Portals Referenced

- **Vidya Lakshmi Portal:** [https://www.vidyalakshmi.co.in](https://www.vidyalakshmi.co.in)
- **Jan Samarth Portal:** [https://www.jansamarth.in](https://www.jansamarth.in)
- **Central Sector Interest Subsidy (CSIS):** [Ministry of Education](https://www.education.gov.in)
- **NCGTC (CGFSEL Scheme):** [https://www.ncgtc.in](https://www.ncgtc.in/en/cgfsel)
- **State Bank of India (SBI):** [https://sbi.co.in](https://sbi.co.in/web/personal-banking/loans/education-loans)
- **Bank of Baroda (BoB):** [https://www.bankofbaroda.in](https://www.bankofbaroda.in/personal-banking/loans/education-loan)

---

## ⚖️ Disclaimer

*EduLoan Guide AI provides financial calculations and guidance based on public Indian Banks' Association (IBA) guidelines. Final loan approvals, interest rates, and margins remain subject to individual bank discretion, RBI repo rates, and official credit appraisals.*

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
