# 💼 FinOps Copilot: Autonomous Finance Controller Agent

An enterprise-ready, verification-first AI Finance Controller Agent designed to automate complex corporate accounting, multi-source reconciliation, and tax compliance auditing. This project implements a complete finance-operations loop that addresses the industry's critical bottleneck: high-precision data verification over large, complex transactional datasets rather than simple data generation.

## 🎯 Project Vision & Core Challenge
Modern finance operations struggle with verifying and reconciling massive volumes of unstructured and structured transactional data. Built to solve this exact verification bottleneck, the **FinOps Copilot** automates:
1. **High-Precision Multi-Source Reconciliation:** Reconciling invoices, payment gateway records, and bank statements.
2. **Tax Compliance Validation:** Ensuring arithmetic accuracy and legal compliance of tax rates.
3. **Liquidity Forecasting:** Delivering forward-looking, real-time corporate cash projection maps.
4. **Interactive Triage:** Empowering users to investigate ledger anomalies through a natural language interface.

---

## ✨ Features Walkthrough

### 1. 🔍 Multi-Source 3-Way Reconciliation
The engine processes and correlates three distinct financial sources to verify payment cycles end-to-end:
*   **Billing Ledger (Invoices):** Expected revenue, customer records, and tax-tier details.
*   **Payment Processor Logs (Gateway):** Instant digital clearance records (e.g., Stripe, UPI) with SUCCESS/FAILURE states.
*   **Corporate Bank Statements (Cleared Cash):** Direct ledger credits (CR) and booking dates representing cleared cash.

### 2. ⚖️ Tax-Line & Arithmetic Integrity Audits
The agent performs granular calculation audits across all billing transactions:
*   Verifies base totals against calculated tax rates (e.g., standard standard corporate GST tiers like 18% or 12%).
*   Flags discrepancies where the invoiced tax amount diverges from the mathematically expected calculation.
*   Highlights compliance anomalies, isolating invoicing errors before month-end book closure.

### 3. 📋 Honest Exception Classification
To streamline human oversight, the system implements an **Honest Exception Ledger**. All discrepancies are isolated, categorized, and fed into an interactive review queue:
*   **Partial Payment / Underpayment:** The customer paid less than the invoiced total.
*   **Duplicate Payment:** Successful gateway transactions double-processed for a single invoice.
*   **Bank/Gateway Discrepancy:** Discrepancies between clearing bank settlements and gateway records (e.g., fee deductions).
*   **Missing Payment:** Raised invoices with no matching processor logs.
*   **Unidentified Bank Transaction:** Direct bank credits that map to no known ledger records.

### 4. 📈 30-Day Predictive Liquidity Forecasting
The forecasting engine builds an interactive, forward-looking cash timeline by:
*   Factoring in current bank balances from reconciled bank statements.
*   Integrating outstanding collections from the Exception Ledger, scheduled to settle on custom terms (e.g., Invoice Date + 30 days).
*   Automating recurring corporate outlays (e.g., SaaS Server Subscriptions, Payroll, Contractor settlements, and Office Rent).

### 5. 💬 Format-Agnostic Conversational Copilot Chat
The dashboard features an interactive conversational assistant to query your financial database:
*   **Database-Driven Lookup:** Scans conversational queries against unique database keys (e.g., invoice IDs). Fully format-agnostic, supporting varied standards (e.g., `INV-083`, `INV-TX-093`, or custom structures) without code changes.
*   **Contextual Explanations:** Explains matching statuses, payment details, and diagnostic reasons for flagged anomalies.

### 👩‍💼 6. Interactive Visual Mascot Companion
To make the dashboard engaging, a cute anime mascot reacts dynamically to your financial health:
*   **Happy State (Match Rate ≥ 90%):** She celebrates high ledger compliance and clean runs.
*   **Focused State (75% ≤ Match Rate < 90%):** She assists with normal corporate triage.
*   **Panic State (Match Rate < 75%):** She displays comic concern, alerting you to heavy transaction anomalies.

---

## 📊 The Presentation Testing Suite

The project includes three pre-compiled, 100-record high-fidelity synthetic testing batches to showcase different operational paths to judges:

| Test Batch | Match Rate | Mascot Expression | Presentation Flow |
| :--- | :--- | :--- | :--- |
| **`invoices.csv`** *(Original)* | **81.73%** | **Focused / Neutral** 📚 | Demonstrates a standard operational day with typical invoice exceptions. |
| **`invoices_test_v2.csv`** *(Test 2)* | **92.00%** | **Happy / Cheering** ✨ | Showcases the "Happy Path" with a highly compliant billing cycle and stellar match rates. |
| **`invoices_test_v3.csv`** *(Test 3)* | **65.00%** | **Comic Panic / Alarm** 😱 | Highlights the "Stress Path," demonstrating robust handling of complex tax anomalies and bank mismatches. |

---

## 🛠️ Installation & Setup

### Prerequisites
Make sure your system has Python installed (v3.10+ recommended) along with the following packages:
```bash
pip install streamlit pandas numpy plotly
```

### Local Workspace Setup
1. Copy your application scripts into your workspace folder:
   ```
   📂 AI Finance Manager/
   ├── finance_copilot_app_v10.py      # Streamlit Dashboard
   ├── finance_controller_agent_v4.py   # AI Matching Engine
   ├── mascot_happy.png                 # Happy Mascot Art
   ├── mascot_neutral.png               # Neutral Mascot Art
   └── mascot_panic.png                 # Panic Mascot Art
   ```
   *(Note: The mascot PNG assets must be placed in this folder to allow local offline rendering without browser-auth issues).*

2. Launch the Streamlit dashboard:
   ```bash
   streamlit run finance_copilot_app_v10.py
   ```

---

## 🛡️ Technical Implementation Details
*   **Dynamic Cache Clearing:** To prevent Streamlit from serving cached data when files with identical filenames (e.g., `temp_invoices.csv`) are uploaded, the "Run Reconciliation" trigger automatically executes a dynamic cache purge (`st.cache_data.clear()`).
*   **Defensive Exception Matching:** The cash forecasting module implements a bulletproof lookup structure that checks if matching invoice records exist in the billing database before accessing `.iloc` references, preventing indexing crashes from orphan payment records or unidentified bank deposits.
