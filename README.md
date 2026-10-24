# 📊 Enterprise HR Analytics & Employee Attrition Intelligence

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14%2B-336791.svg)](https://www.postgresql.org/)
[![Power BI](https://img.shields.io/badge/Power_BI-Desktop-F2C811.svg)](https://powerbi.microsoft.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An end-to-end, enterprise-grade **People Analytics & Workforce Intelligence** project analyzing employee attrition drivers, compensation equity, operational workload, attendance, and retention risk modeling across 326 workforce profiles.

---

## 🎯 Executive Summary & Core Results

| Executive KPI | Value | Benchmark / Variance | Strategic Implications |
| :--- | :--- | :--- | :--- |
| **Total Workforce** | **326 Staff** | Active: 235 \| Left: 91 | Core sample size |
| **Overall Attrition Rate** | **27.91%** | Benchmark: 15-18% | Elevated organizational departure rate |
| **Highest Attrition Department** | **Human Resources (46.15%)** | Sales: 31.25% \| R&D: 25.35% | Severe HR division talent drain |
| **Highest Risk Role** | **Sales Rep (57.14%)** | Lab Tech: 38.75% | Entry-level commercial turnover |
| **Overtime Attrition Multiplier** | **56.38% vs 16.38%** | **3.4x Risk Factor** ($p = 2.30 \times 10^{-10}$) | Primary operational burnout driver |
| **Compensation Disparity** | **$2,515 vs $3,375** | **$860/mo Median Deficit** ($p < 0.001$) | Low salary triggers early departures |
| **Critical Risk Segment** | **62.50% Attrition** | Overtime + Low Pay + Low Sat | 32 staff require immediate retention plan |
| **Model Predictive AUC** | **0.692 ROC-AUC** | Recall: 61% on Attrited cohort | Identifies at-risk talent proactively |

---

## 🏗️ Repository Architecture

```
hr-analytics/
├── data/
│   ├── raw/
│   │   └── hr_employee_data_raw.csv        # Raw dataset with original fields
│   └── processed/
│       ├── fact_hr_analytics.csv           # Cleaned central analytical fact table
│       ├── dim_department.csv              # Dimension: Department lookup
│       ├── dim_job_role.csv                # Dimension: Job role & department mapping
│       ├── dim_age_group.csv               # Dimension: Age brackets
│       └── dim_satisfaction.csv            # Dimension: Likert satisfaction scale
├── sql/
│   ├── schema.sql                          # PostgreSQL DDL table creation & indexing
│   ├── data_quality_checks.sql             # SQL data integrity, duplicate & boundary tests
│   ├── kpi_analysis.sql                    # Executive KPI calculations & cohort comparisons
│   ├── department_analysis.sql             # Departmental breakdowns, role pay & window ranking
│   └── attrition_analysis.sql              # Multi-factor risk queries & risk tier CTE
├── notebooks/
│   └── hr_eda.ipynb                        # 11-stage Jupyter notebook with complete EDA & ML
├── src/
│   ├── generate_dataset.py                 # Synthetic benchmark dataset generator (seed=42)
│   ├── data_cleaning.py                    # Data validation, cleaning, and Star Schema export
│   ├── analysis.py                         # SQL query execution & statistical hypothesis testing
│   ├── generate_charts_and_model.py        # High-res visualization and Scikit-learn modeling
│   └── create_notebook.py                  # Programmatic generator for notebooks/hr_eda.ipynb
├── outputs/
│   ├── charts/                             # 9 high-resolution analytical chart exports (PNG)
│   └── reports/                            # KPI summaries, department metrics, model metrics (CSV)
├── powerbi/
│   ├── data_model.md                       # Star schema diagram, table cardinalities & keys
│   ├── dax_measures.md                     # Complete DAX measures library with format strings
│   └── dashboard_guide.md                  # 4-page dashboard specification & step-by-step guide
├── docs/
│   ├── data_dictionary.md                  # Field descriptions, data types, domains, and business rules
│   ├── methodology.md                      # Data engineering, SQL, and statistical methodology
│   └── findings_and_recommendations.md     # Detailed business findings & 4-pillar action plan
├── requirements.txt                        # Python dependencies
├── .gitignore                              # Git exclusion rules
└── README.md                               # Project documentation & execution guide
```

---

## 🛠️ Technology Stack

- **SQL:** PostgreSQL (ANSI SQL compliant) — CTEs, Window Functions (`DENSE_RANK`, `NTILE`, `AVG OVER`), multi-level aggregations.
- **Python:** Python 3.10+ — `pandas` (cleaning/transformation), `numpy` (vectorized math), `matplotlib` & `seaborn` (visualization), `scipy` (Mann-Whitney U, Chi-Square testing), `scikit-learn` (interpretable logistic regression, ROC-AUC).
- **Power BI:** Star Schema data modeling, DAX measures, dynamic title cards, 4-page executive reporting.
- **Git/GitHub:** Version control, structured documentation, and reproducibility.

---

## ⚡ Quickstart & Execution Guide

### 1. Prerequisites & Virtual Environment Setup
Ensure Python 3.10+ is installed on your workstation.

```bash
# Clone the repository
git clone https://github.com/your-username/hr-analytics.git
cd hr-analytics

# Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Execute Data Pipeline & Cleaning
```bash
# Run data cleaning and export Power BI star schema tables
python src/data_cleaning.py
```

### 3. Run Analytical SQL Queries & Hypothesis Tests
```bash
# Executes SQL test suite and outputs KPI verification reports
python src/analysis.py
```

### 4. Generate Visualizations & Machine Learning Models
```bash
# Generates all charts into outputs/charts/ and evaluates logistic regression
python src/generate_charts_and_model.py
```

### 5. Launch the Jupyter Notebook
```bash
jupyter notebook notebooks/hr_eda.ipynb
```

---

## 🗄️ SQL Analysis Highlights

The project contains complete SQL scripts in `sql/` ready to run against PostgreSQL, MySQL 8.0, or SQLite:

### Sample: Executive KPI Calculation (`sql/kpi_analysis.sql`)
```sql
WITH ExecutiveKPIs AS (
    SELECT
        COUNT(*) AS total_employees,
        SUM(CASE WHEN attrition = 'No' THEN 1 ELSE 0 END) AS active_employees,
        SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS employees_who_left,
        ROUND((SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) / COUNT(*)) * 100, 2) AS overall_attrition_rate_pct,
        ROUND(AVG(salary), 2) AS avg_monthly_salary,
        ROUND((SUM(CASE WHEN overtime = 'Yes' THEN 1.0 ELSE 0 END) / COUNT(*)) * 100, 2) AS overtime_pct,
        ROUND(AVG(attendance_rate), 2) AS avg_attendance_rate_pct
    FROM hr_employees
)
SELECT * FROM ExecutiveKPIs;
```

### Sample: Department Salary Rank & Variance Window Function (`sql/department_analysis.sql`)
```sql
WITH RoleDeptPay AS (
    SELECT 
        department,
        job_role,
        COUNT(*) AS role_headcount,
        ROUND(AVG(salary), 2) AS role_avg_salary
    FROM hr_employees
    GROUP BY department, job_role
)
SELECT 
    department,
    job_role,
    role_headcount,
    role_avg_salary,
    ROUND(AVG(role_avg_salary) OVER(PARTITION BY department), 2) AS dept_benchmark_avg_salary,
    ROUND(role_avg_salary - AVG(role_avg_salary) OVER(PARTITION BY department), 2) AS variance_from_dept_mean,
    DENSE_RANK() OVER(PARTITION BY department ORDER BY role_avg_salary DESC) AS pay_rank_in_department
FROM RoleDeptPay
ORDER BY department, pay_rank_in_department;
```

---

## 📈 Power BI 4-Page Dashboard Overview

The dashboard specification in `powerbi/dashboard_guide.md` and DAX formulas in `powerbi/dax_measures.md` detail:
- **Page 1: HR Overview:** KPI scorecards, headcount vs attrition by department, role breakdown, and age group slicers.
- **Page 2: Attrition Analysis:** Overtime attrition multiplier, salary band distribution, job satisfaction vs work-life balance risk matrix.
- **Page 3: Performance & Workforce:** Salary vs experience scatter curve, department appraisal scores, absenteeism distribution.
- **Page 4: Strategic Recommendations:** Critical risk segment callout (62.5% attrition), 4-pillar retention roadmap, and data limitations.

---

## 💼 Resume & Portfolio Bullet Points

Use these high-impact bullet points on your Data Analyst resume or LinkedIn:

- **End-to-End Analytics Pipeline:** Built an end-to-end HR Analytics pipeline in Python and SQL analyzing 326 employee profiles, isolating key attrition drivers, and exporting Star Schema tables for Power BI reporting.
- **Advanced SQL & Window Functions:** Authored PostgreSQL scripts utilizing CTEs, window functions (`DENSE_RANK`, `NTILE`, `AVG OVER`), and data quality test suites to compute 14 organizational KPIs with 100% denominator consistency.
- **Statistical Significance & Modeling:** Conducted Mann-Whitney U and Chi-Square tests establishing Overtime ($p = 2.30 \times 10^{-10}$) and Base Salary ($p < 0.001$) as primary departure drivers; trained an interpretable Logistic Regression model achieving 0.692 ROC-AUC and 61% recall.
- **Business Impact & Decision Support:** Formulated a 4-pillar strategic retention roadmap targeting a 32-person critical risk cohort (62.5% attrition), providing HR executive leadership with actionable overtime caps and compensation adjustments.

---

## 📜 License & Acknowledgments

This project is licensed under the MIT License. Built using standard HR analytics benchmarking methodologies.
