# Executive Findings & Strategic HR Recommendations Report

**Target Audience:** Chief Human Resources Officer (CHRO), VP of Talent Management, People Analytics Steering Committee  
**Data Scope:** 326 Employee Records across Human Resources, Research & Development, and Sales  
**Analytical Engine:** PostgreSQL / SQLite, Python (Pandas/Scipy/Scikit-learn), Power BI Desktop

---

## 1. Executive Summary & Key Measured Results

A diagnostic analysis of workforce data reveals an overall organizational attrition rate of **27.91%** (91 departed out of 326 total employees). Attrition is non-uniform across the company: it is heavily concentrated in specific departments, operational workload configurations, and compensation brackets.

| Core Metric / KPI | Organization-Wide Value | Attrition = Yes (Departed) | Attrition = No (Retained) | Statistical Significance |
| :--- | :--- | :--- | :--- | :--- |
| **Total Headcount** | 326 Employees | 91 (27.91%) | 235 (72.09%) | — |
| **Median Monthly Salary** | $3,161.50 | **$2,515.00** | **$3,375.00** | Significant ($p = 6.58 \times 10^{-6}$) |
| **Overtime Exposure Rate** | 28.83% | **58.24% of leavers** | **17.45% of retained** | Significant ($p = 2.30 \times 10^{-10}$) |
| **Average Tenure at Company**| 4.05 Years | 3.22 Years | 4.38 Years | Significant ($p = 0.012$) |
| **Average Attendance Rate** | 96.12% | 96.04% | 96.16% | Baseline uniform |
| **Promotion in Last 3 Yrs** | 94.17% | 93.41% | 94.47% | Not significantly divergent |

---

## 2. Answers to Core Business Questions

### Question 1: Which departments have the highest attrition rates?
**Measured Result:**
1. **Human Resources:** **46.15% Attrition** (6 departed out of 13 employees). Lowest departmental average salary ($3,070.31).
2. **Sales:** **31.25% Attrition** (30 departed out of 96 employees). Characterized by high travel frequency and client-facing quota stress.
3. **Research & Development:** **25.35% Attrition** (55 departed out of 217 employees). While representing the largest absolute headcount, R&D maintains the lowest relative departure rate.

### Question 2: Which employee groups and job roles show higher attrition?
**Measured Result:**
- **Job Role Vulnerability:**
  - `Sales Representative`: **57.1% Attrition Rate** (12 departed out of 21). Average salary: $2,580/month.
  - `Laboratory Technician`: **38.8% Attrition Rate** (31 departed out of 80). Average salary: $2,955/month.
  - `Human Resources Specialist`: **46.2% Attrition Rate** (6 departed out of 13).
  - Conversely, `Manager` (4.2%) and `Research Director` (5.6%) exhibit exceptional retention stability.
- **Demographic Cohort:**
  - **Age < 25:** **48.3% Attrition Rate** (highest across age brackets).
  - **Single Employees:** **39.4% Attrition Rate** vs Married (22.8%) and Divorced (22.5%). Single employees have higher geographic and career mobility.

### Question 3: How are salary, tenure, overtime, and satisfaction associated with attrition?
**Measured Result:**
1. **Overtime (The Strongest Statistical Driver):**
   - Employees working Overtime experience an attrition rate of **56.38%** (53 out of 94).
   - Employees with No Overtime experience an attrition rate of **16.38%** (38 out of 232).
   - $\chi^2 = 40.20, p < 0.0001$. An employee assigned to overtime is **3.4 times more likely to leave**.
2. **Salary Banding:**
   - `< $3,500 (Entry)`: **41.72% Attrition Rate** (73 departed out of 175).
   - `$3,500 - $6,999 (Mid)`: **13.56% Attrition Rate** (16 departed out of 118).
   - `$7,000+ (Senior/Exec)`: **6.06% Attrition Rate** (2 departed out of 33).
3. **Tenure at Company:**
   - First year (`< 1 Year`): **46.15% Attrition Rate**.
   - Years 1-2: **34.88% Attrition Rate**.
   - Years 6+: Attrition stabilizes below 18%.
4. **Job Satisfaction:**
   - Low Satisfaction (1): **35.0% Attrition Rate**.
   - Very High Satisfaction (4): **22.5% Attrition Rate**.
   - While satisfaction alone showed $p = 0.19$, when interacted with Overtime, low satisfaction acts as a severe departure accelerator.

### Question 4: Which departments have the highest average performance ratings?
**Measured Result:**
- **Sales:** 3.15 / 4.00
- **Research & Development:** 3.14 / 4.00
- **Human Resources:** 3.08 / 4.00
All three departments maintain a healthy appraisal score centered near corporate benchmark targets (3.10-3.15). Crucially, departing employees are **not** poor performers (mean rating for departed employees is 3.15 vs 3.14 for retained). The organization is losing high-performing contributors.

### Question 5: Is there an association between promotion history and attrition?
**Measured Result:**
- Promotion within the last 3 years is widespread in this sample (**94.17% overall**), reflecting an active internal mobility cadence.
- As a result, lack of promotion is **not** the primary driver of attrition in this cohort ($p > 0.05$). Attrition is overwhelmingly driven by current operational workload (overtime) and baseline compensation rather than promotion frequency.

### Question 6: What workforce patterns deserve immediate management attention?
**Measured Result:**
The analytical model isolated a **Critical Risk Segment**:
$$\text{Criteria: } \text{Overtime} = \text{'Yes'} \quad\text{AND}\quad \text{Salary} < \$5,000 \quad\text{AND}\quad \text{JobSatisfaction} \le 2$$
- **Cohort Size:** 32 Employees
- **Attrition Count:** 20 Departures
- **Cohort Attrition Rate:** **62.50%**
This subset represents an acute operational vulnerability requiring immediate retention intervention.

---

## 3. Actionable HR Recommendations

### Pillar 1: Overtime Normalization & Workload Governance (Immediate / 30 Days)
- **Problem:** Overtime drives attrition from 16.4% to 56.4%.
- **Action:**
  1. Institute a hard cap of 8 overtime hours per week per employee in Laboratory and Sales operations.
  2. Implement a mandatory compensatory off (comp-off) policy where overtime hours are credited as additional rest days within 30 days.
  3. Rebalance laboratory technician shift staffing by hiring additional shift coverage to distribute testing volume.

### Pillar 2: Entry-Level Compensation Equity Audit (Medium-Term / 60-90 Days)
- **Problem:** Attrition in the `< $3,500` salary band is 41.72% (median salary of departed staff is $2,515 vs $3,375 for retained).
- **Action:**
  1. Adjust entry baseline compensation for `Sales Representative` and `Laboratory Technician` roles toward the $3,200-$3,500 threshold.
  2. Restructure Sales Representative compensation to increase fixed base pay by 15%, reducing reliance on volatile commission targets.

### Pillar 3: First-Year "Flight-Risk" Onboarding & Mentorship (60 Days)
- **Problem:** 46.15% of employees in their first year at the company depart.
- **Action:**
  1. Deploy a structured "Buddy & Mentor" program pairing new hires under age 25 with senior staff (tenure > 5 years).
  2. Schedule 30-day, 60-day, and 90-day sentiment check-ins led by HR Business Partners to identify workload stress early.

### Pillar 4: Targeted Retention in Human Resources (Immediate)
- **Problem:** HR has the highest department attrition (46.15%) and lowest compensation ($3,070).
- **Action:**
  1. Review administrative burden and tooling automation in the HR department to reduce manual documentation fatigue.
  2. Benchmark HR salaries against cross-departmental administrative peers.

---

## 4. Analytical Limitations & Assumptions

> [!NOTE]
> - **Cross-Sectional Dataset:** This analysis evaluates observational cross-sectional data; statistical association does not definitively prove causation.
> - **Unobserved Exogenous Factors:** External macroeconomic job market offers, competitor wage increases, and commute changes were not measured.
> - **Recommendation:** Deploy quarterly pulse surveys and standardized exit interview tracking to enrich quantitative findings with qualitative sentiment data.
