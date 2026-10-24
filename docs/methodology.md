# HR Analytics & Workforce Intelligence: End-to-End Methodology

## 1. Project Analytical Lifecycle

This project executes a rigorous, multi-tiered analytics workflow designed to simulate an enterprise People Analytics deployment:

```
+--------------------+      +--------------------+      +---------------------+
| 1. Data Ingestion  | ---> | 2. Data Cleaning   | ---> | 3. SQL Architecture |
| - Raw CSV audit    |      | - Deduplication    |      | - Schema & DDL      |
| - Validation tests |      | - Bins & Features  |      | - CTEs & Windows    |
+--------------------+      +--------------------+      +---------------------+
                                                                   |
                                                                   v
+--------------------+      +--------------------+      +---------------------+
| 6. Power BI BI     | <--- | 5. Statistical EDA | <--- | 4. Star Schema DWH  |
| - 4-page dashboard |      | - Hypothesis tests |      | - Fact & Dimensions |
| - Dynamic DAX      |      | - Interpretable ML |      | - Single 1:* filters|
+--------------------+      +--------------------+      +---------------------+
```

---

## 2. Data Pipeline & Transformation Architecture

### 2.1 Ingestion & Cleaning
- **Raw Audit:** Raw data imported and inspected for encoding, missing values, string anomalies, and duplicate identifiers.
- **Normalization:** Inconsistent string inputs (e.g. `TravelRarely` to `Travel_Rarely`) standardized.
- **Standardized Nomenclature:** Columns aligned to universal enterprise HR schemas (`EmployeeID`, `Salary`, `YearsOfExperience`, `PromotionHistory`, `Overtime`).

### 2.2 Feature Engineering & Categorical Binning
To support multi-dimensional slicing in Power BI and analytical aggregations in SQL:
- **`AgeGroup`:** Categorized into chronological brackets (`<25`, `25-34`, `35-44`, `45-54`, `55+`).
- **`SalaryBand`:** Segmented by monthly compensation brackets (`< $3,500 (Entry)`, `$3,500 - $6,999 (Mid)`, `$7,000 - $11,999 (Senior)`, `$12,000+ (Executive)`).
- **`ExperienceBand` & `TenureBand`:** Stratified to evaluate early-career flight risk vs tenured retention.
- **`AttendanceRate` & `AbsenceDays`:** Operationalized based on standard 250 corporate working days per annum.

---

## 3. SQL Query Design Principles

All analytical scripts are written in standard ANSI SQL with PostgreSQL and MySQL compatibility:
1. **Common Table Expressions (CTEs):** Used to decompose complex business logic into readable, maintainable logical modules (e.g., `EmployeeRiskProfile` in `attrition_analysis.sql`).
2. **Window Functions:** Leveraged for intra-department compensation ranking (`DENSE_RANK() OVER(PARTITION BY department ORDER BY salary DESC)`) and departmental benchmark variance (`AVG(...) OVER(PARTITION BY department)`).
3. **Denominator Consistency:** Across all queries, the denominator for attrition rate is strictly the total cohort population in the filter scope:
   $$\text{Attrition Rate} = \frac{\sum \text{Departed Employees}}{\text{Total Headcount}} \times 100$$
4. **Data Preservation:** Queries use filtering and aggregation without dropping raw records from storage.

---

## 4. Statistical Testing Methodology

To prevent attributing random sampling variance to business drivers, empirical hypothesis testing was conducted:
1. **Mann-Whitney U Test (Salary by Attrition):** Non-parametric rank-sum test selected due to positive skewness in compensation distributions ($p < 0.001$, confirming departed employees earn significantly lower median salaries).
2. **Chi-Square ($\chi^2$) Test of Independence (Overtime vs Attrition):** Contingency table test evaluating whether attrition is independent of overtime status ($\chi^2 = 40.20, p = 2.30 \times 10^{-10}$, proving extreme dependence).
3. **Chi-Square Test (Job Satisfaction vs Attrition):** Assesses whether satisfaction rating alone explains departures ($p = 0.19$, demonstrating that satisfaction acts primarily as an interactive compounder rather than an isolated predictor).

---

## 5. Machine Learning Methodology & Data Leakage Prevention

### 5.1 Leakage Prevention
- Target column (`AttritionNumeric`) and active flags (`IsActive`) excluded from model feature matrix.
- Preprocessing steps (StandardScaler, OneHotEncoder) fitted strictly on training data within a Scikit-learn `Pipeline` to prevent test-set data leakage.

### 5.2 Training & Evaluation
- **Split:** 80% Train, 20% Test with stratified sampling to preserve the 27.9% attrition prevalence.
- **Model Choice:** L2-regularized **Balanced Logistic Regression** selected specifically for model interpretability. Class weights balanced to handle minority class penalty.
- **Evaluation Metrics:** ROC-AUC ($0.692$) and Recall ($61\%$) prioritized over raw accuracy because false negatives (unidentified at-risk talent) carry substantial organizational replacement costs.
- **Interpretability:** Model coefficients converted to **Odds Ratios** ($e^\beta$) to provide HR leaders with clear risk multipliers.

---

## 6. Power BI Implementation Architecture

1. **Star Schema Data Modeling:** 1-to-many single-directional relationships from `dim_department`, `dim_job_role`, `dim_age_group`, and `dim_satisfaction` to `fact_hr_analytics`.
2. **Measure Encapsulation:** Dedicated `_Measures` table housing all DAX calculations to ensure central maintainability and avoid implicit column measures.
3. **Responsive UX:** 4-page structured narrative transitioning from high-level executive KPIs to deep-dive root causes, workforce talent dynamics, and strategic management actions.
