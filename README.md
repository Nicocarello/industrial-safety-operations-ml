# TechnoStamp Industries: Strategic Workforce & Operational Analytics
### A Decision Science & Machine Learning Case Study for C-Level Advisory

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![LightGBM](https://img.shields.io/badge/Model-LightGBM%20(ROC--AUC%200.88)-green.svg)](https://lightgbm.readthedocs.io/)
[![Dashboard](https://img.shields.io/badge/Interactive-Executive%20Dashboard%20(HTML%2FJS)-teal.svg)](dashboard_ejecutivo.html)
[![Presentation](https://img.shields.io/badge/Deck-Executive%2016%3A9%20(PPTX)-navy.svg)](Presentacion_Directorio_TechnoStamp.pptx)

---

## 📌 Executive Summary

**TechnoStamp Industries** is a 15-year-old manufacturing company with ~450–580 employees facing critical operational challenges: chronic scrap rates, escalating overtime costs, recurring plant accidents, and voluntary turnover. 

Historically, management decisions were driven by intuition. This project demonstrates how an end-to-end **Decision Science & Advanced People Analytics** approach transforms raw operational and HR tables into an **audit-proof strategic turnaround plan**, delivering an estimated **net annualized EBITDA upside of >$363 Million ARS**.

---

## 🏗️ Project Architecture & Deliverables

```text
├── assets/
│   ├── figures/                       # High-resolution (300 DPI) publication-ready charts
│   ├── metrics_summary.json           # Consolidated operational & statistical metrics
│   ├── ml_models_summary.json         # Benchmarks & feature importance for 3 ML models
│   └── models/                        # Serialized LightGBM pipelines in production
│       ├── model_safety_risk_lgbm.pkl # Safety Early Warning (ROC-AUC 0.88)
│       ├── model_flight_risk_lgbm.pkl # Voluntary Churn Predictor (ROC-AUC 0.73)
│       └── model_high_scrap_lgbm.pkl  # Predictive Quality Risk (ROC-AUC 0.96)
├── data/                              # Panel data (employees monthly, events, training)
├── src/
│   ├── analysis_pipeline.py           # Unified reproducible analytical & statistical pipeline
│   ├── train_ml_suite.py              # Full 3-model Machine Learning training & evaluation suite
│   ├── generate_charts.py             # Script generating executive visual charts
│   └── create_presentation.py         # Automated PPTX deck generation script
├── dashboard_ejecutivo.html           # Interactive HTML5/JS dashboard with real-time ROI simulator
├── Presentacion_Directorio_TechnoStamp.pptx # Official 7-slide 16:9 Board of Directors deck
├── INFORME_EJECUTIVO_TECHNOSTAMP.md   # Comprehensive executive master report
└── README.md                          # Repository overview & portfolio guide
```

---

## 🔍 Key Findings & Forensic Discoveries

### 1. The Night Shift Crisis & Scrap Crunch
* **The Problem:** Night shift scrap is **3.60%** vs **1.79%** on day shifts (**+101.1%**, $t = 42.17$, $p < 0.0001$), generating **71.4% of total factory scrap-lost days (1,757 days)** and >18,600 excess defective parts.
* **Severe Accident Hub:** Night shift concentrates **55.6% of all accidents** and **83.3% of severe incidents** (11.77 vs 2.22 per 1,000 emp-months, **5.31x relative risk**).
* **Forensic Root Cause:** Zero Level 3/4 managers or supervisors on site during the night shift. Furthermore, in **June–August 2024**, scrap spiked to **4.78%** in Estampado (5.45% in Setup), which triggered the dismissal of Plant Manager Damián Barbieri (ID 1001) in Dec 2024. The Plant Manager seat **remained completely vacant in 2025**.

### 2. The Succession Cliff & Argentine Labor Law Blindspot
* **Critical Exposure:** **4 out of 5 active critical positions (80%) retire within $\le 12$ months**.
* **Total Deprivation in Logistics:** The entire managerial spine in Logistics (Supervisor Ana Ortiz in 6m, Team Leaders Sergio Reyes in 9m and Miguel De Luca in 12m) is leaving within a year.
* **The Legal Blindspot:** The legacy HR system calculated retirement assuming 65 years for all personnel. Under Argentine Labor Law (Ley 24.241), women retire at **60 years**.
  * **Teresa Rodríguez (64 years old, Setup in Estampado, 11.3 years of experience)** is already 4 years past legal retirement age and has no designated successor.
* **ERP Data Hygiene:** Uncovered that 6 employees aged 26–45 were misclassified as "Jubilación" due to legacy payroll tagging bugs.

### 3. The Overtime Spiral ($1.422M ARS) vs. 67-Day Time-to-Fill
* **The Spend:** **$1.422 Billion ARS** spent across 98,260 overtime hours. 99.8% of shopfloor employees clock overtime every single month.
* **The Driver:** Overtime is not caused by sales spikes; it is driven by recruitment lag. Time-to-Fill in Maintenance averages **66.6–70.9 days** (peaking at **144 days for Industrial Electricians**).
* **The "Toxic Manager" Cluster:** Voluntary turnover is hyper-concentrated in 4 specific supervisors with **60%–80% team resignation rates** (Alan Marino, Facundo Ricci, Isaías Peña, Luciano Chávez) due to chronic fatigue.

### 4. Safety Data Hygiene & The Machine Learning Early-Warning Engine
* **Incident Discrepancy Clarified:** 100 monthly incident occurrences vs 45 events in the transactional log. Forensic audit confirmed that 55 were minor internal first-aid clinic entries (zero lost workdays), whereas 45 were formal lost-time ART insurance claims (138 lost days).
* **Fatigue Tipping Point:** Working **>20 overtime hours/month** causes accident probability to spike from **0.63% to 3.40% (a 5.4x jump)**.
* **The Training Mismatch:** **78.0% of accident victims never received safety training**.
* **LightGBM Predictive Classifier:**
  * Engineered rolling fatigue features, ratio of overtime to safety training hours, tenure, and department.
  * Achieved **ROC-AUC of 0.8758**.
  * **Operational Lift:** Targeting the top 20% highest-risk workers allows management to capture **83.3% of all upcoming workplace accidents**.

### 5. Gender Diversity, Meritocracy & The Level 4 Salary Gap
* **Representation:** 37.0% female workforce, but with strong horizontal segregation in Assembly (26.8%) and Engineering (28.6%), with 0 women in Process Engineering.
* **Performance:** Women demonstrate higher average performance ratings (**3.26 vs 3.17**, $p = 0.016$) and a higher percentage of *Top Performers* (**9.1% vs 7.3%**).
* **Salary Equity:** Strict pay equity in base and mid-level roles (Levels 1–3, gap < 1%), but a **7.3% salary gap favoring men at Level 4 (Department Managers)**.

---

## 💰 Financial Quantification: +$363M ARS Annual EBITDA Upside

| Initiative | Baseline | 12-Month Target | Net EBITDA Gain |
| :--- | :---: | :---: | :---: |
| **Night Shift Scrap Containment** | 3.60% scrap rate | 2.00% scrap rate | **+$125M ARS** |
| **Overtime Rationalization** | 98.2k hours ($1.004M/yr) | 25% reduction via hiring | **+$251M ARS** |
| **Accident Mitigation & ART Insurance** | 45 ART lost-time events | <15 events (ML early warning) | **+$9M ARS** |
| **Implementation Program Costs** | Training, recruiting fees, incentives | Comprehensive roadmap | **-$22M ARS** |
| **NET ANNUALIZED EBITDA IMPACT** | | | **>+$363M ARS** |

---

## 🚀 30-60-90 Day Strategic Action Plan

```
[0-30 Days: Crisis Containment]
├── Deploy 2 rotating Level 3 Supervisors to the Night Shift.
├── Launch emergency 90-day shadow apprenticeship for Teresa Rodríguez & Logistics.
├── Fill the vacant Plant Manager (Level 5) position immediately.
└── HR climate intervention with the 4 high-turnover supervisors.

[31-60 Days: Tactical Stabilization]
├── Build technical partnerships (UTN / vocational schools) to slash Time-to-Fill to <25 days.
├── Implement mandatory Safety & Machine Lockout (LOTO) certification for 100% of plant staff.
├── Enforce strict hard-cap of 15 overtime hours/month per operator.
└── Update ERP retirement formula to 60 years for women (Ley 24.241).

[61-90+ Days: Institutionalization & Early Warning]
├── Deploy production LightGBM predictive risk score on shopfloor executive screens.
├── Close the 7.3% salary gap in Level 4 and promote Top Performer women to Team Leaders.
└── Realign supervisor quarterly bonuses (30% tied to scrap <2.0% and zero lost-time accidents).
```

---

## 💻 How to Run Locally

### 1. Prerequisites
```bash
pip install pandas numpy scipy matplotlib seaborn python-pptx scikit-learn lightgbm joblib
```

### 2. Run Full Analytics & ML Pipeline
```bash
python src/analysis_pipeline.py
```
*Outputs model artifact `assets/technostamp_safety_model_prod.pkl` and `assets/metrics_summary.json`.*

### 3. Generate Visual Assets & Deck
```bash
python src/generate_charts.py
python src/create_presentation.py
```

### 4. Open Interactive Dashboard
Simply double-click or serve `dashboard_ejecutivo.html` in any web browser.

---

## 👤 Author & Contact
* **Author:** Nicolás Carello Laje
* **GitHub Repository:** [Nicocarello/industrial-safety-operations-ml](https://github.com/Nicocarello/industrial-safety-operations-ml)
* **Specialization:** Data Analyst | Data Scientist | Machine Learning
* **Focus:** Data-driven operational turnarounds, econometric modeling, industrial analytics, and executive storytelling.
* **Portfolio Showcase:** Ready for deployment and live board presentations.
