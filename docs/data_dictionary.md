# HR Analytics: Data Dictionary & Field Catalog

## 1. Overview & Provenance

This dataset captures workforce demographic, operational, compensatory, attendance, satisfaction, performance, and attrition records. The dataset is structured for analytical SQL queries, Python exploratory data analysis and predictive modeling, and star-schema reporting in Power BI.

- **Primary Entity:** Employee Profile (`fact_hr_analytics`)
- **Primary Identifier:** `EmployeeID`
- **Total Records:** 326 employees
- **Grain:** One record per individual employee

---

## 2. Comprehensive Field Catalog

| Column Name | SQL Data Type | Python Dtype | Description | Allowed Values / Domain | Business Purpose | Sample Value |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`EmployeeID`** | VARCHAR(20) | string | Unique primary key identifying the employee | `EMP0001` or `RM001`-`RM1470` | Unambiguous record lookup | `RM297` |
| **`Age`** | INT | int64 | Age in completed years | 18 to 60 | Demographic analysis | `28` |
| **`AgeGroup`** | VARCHAR(20) | string / cat | Binned chronological age bracket | `<25`, `25-34`, `35-44`, `45-54`, `55+` | Demographic slicing & reporting | `25-34` |
| **`Gender`** | VARCHAR(10) | string | Self-reported gender identity | `Male`, `Female` | Workforce diversity auditing | `Female` |
| **`MaritalStatus`**| VARCHAR(20) | string | Marital status of the employee | `Single`, `Married`, `Divorced` | Life-stage & mobility analysis | `Single` |
| **`Department`** | VARCHAR(50) | string | Functional division within the organization | `Sales`, `Research & Development`, `Human Resources` | Departmental performance & cost center tracking | `Sales` |
| **`JobRole`** | VARCHAR(50) | string | Specific professional job title | `Sales Executive`, `Research Scientist`, `Laboratory Technician`, `Manufacturing Director`, `Healthcare Representative`, `Manager`, `Sales Representative`, `Research Director`, `Human Resources` | Role-level benchmark & retention | `Sales Executive` |
| **`EducationField`**| VARCHAR(50) | string | Primary academic specialization | `Life Sciences`, `Medical`, `Marketing`, `Technical Degree`, `Human Resources`, `Other` | Skill matching & talent acquisition | `Life Sciences` |
| **`Salary`** | NUMERIC(10,2)| int64 | Base monthly gross income (USD) | $1,000 to $20,000 | Compensation analysis | `4850` |
| **`AnnualSalary`** | NUMERIC(12,2)| int64 | Base annual gross salary (`Salary * 12`) | $12,000 to $240,000 | Annual budgeting & financial reporting | `58200` |
| **`SalaryBand`** | VARCHAR(50) | string / cat | Monthly income tier | `< $3,500 (Entry)`, `$3,500 - $6,999 (Mid)`, `$7,000 - $11,999 (Senior)`, `$12,000+ (Executive)` | Compensation band comparison | `< $3,500 (Entry)` |
| **`YearsOfExperience`** | INT | int64 | Total career working experience (years) | 0 to 40 | Career maturity benchmark | `6` |
| **`ExperienceBand`** | VARCHAR(50) | string / cat | Career experience bracket | `0-2 Years`, `3-5 Years`, `6-10 Years`, `11-20 Years`, `20+ Years` | Experience cohort tracking | `3-5 Years` |
| **`YearsAtCompany`** | INT | int64 | Tenure at current enterprise (years) | 0 to 40 (`<= YearsOfExperience`) | Retention & tenure benchmarking | `4` |
| **`TenureBand`** | VARCHAR(50) | string / cat | Enterprise tenure bracket | `< 1 Year`, `1-2 Years`, `3-5 Years`, `6-10 Years`, `10+ Years` | Early flight risk analysis | `3-5 Years` |
| **`AttendanceRate`**| NUMERIC(5,2)| float64 | Percentage of annual working days present | 75.00% to 100.00% | Operational attendance KPI | `96.40` |
| **`AbsenceDays`** | INT | int64 | Total scheduled and unscheduled absent days | 0 to 25 days (based on 250 working days) | Absenteeism diagnostic | `9` |
| **`Overtime`** | VARCHAR(5) | string | Regular overtime engagement status | `Yes`, `No` | Workload exposure & burnout driver | `Yes` |
| **`JobSatisfaction`**| INT | int64 | Standard Likert satisfaction score | 1 (Low), 2 (Medium), 3 (High), 4 (Very High) | Employee sentiment metric | `3` |
| **`JobSatisfactionLabel`** | VARCHAR(50) | string | Text label for satisfaction score | `1 - Low`, `2 - Medium`, `3 - High`, `4 - Very High` | Power BI slicers & tooltips | `3 - High` |
| **`PerformanceRating`**| INT | int64 | Annual appraisal evaluation score | 1 (Low), 2 (Good), 3 (Excellent), 4 (Outstanding) | Talent quality evaluation | `3` |
| **`PerformanceRatingLabel`** | VARCHAR(50) | string | Text label for appraisal score | `1 - Low`, `2 - Good`, `3 - Excellent`, `4 - Outstanding` | Reporting clarity | `3 - Excellent` |
| **`PromotionHistory`** | INT | int64 | Number of years elapsed since last promotion | 0 to 15 (`<= YearsAtCompany`) | Career velocity & stagnation tracking | `1` |
| **`PromotionInLast3Years`** | VARCHAR(5) | string | Flag indicating promotion within last 36 months | `Yes`, `No` | Promotion rate calculation | `Yes` |
| **`WorkLifeBalance`** | INT | int64 | Perceived work-life balance rating | 1 (Bad), 2 (Good), 3 (Better), 4 (Best) | Wellbeing diagnostic | `2` |
| **`WorkLifeBalanceLabel`** | VARCHAR(50) | string | Descriptive label for work-life balance | `1 - Bad`, `2 - Good`, `3 - Better`, `4 - Best` | Reporting visualization | `2 - Good` |
| **`TrainingHours`** | INT | int64 | Total hours of training completed in past year | 8 to 80 hours | Talent upskilling & development ROI | `36` |
| **`BusinessTravel`**| VARCHAR(50) | string | Frequency of job-related travel | `Non-Travel`, `Travel_Rarely`, `Travel_Frequently` | Travel burden analysis | `Travel_Rarely` |
| **`Attrition`** | VARCHAR(5) | string | Primary target: whether employee departed | `Yes`, `No` | Attrition measurement & labeling | `No` |
| **`AttritionNumeric`** | INT | int64 | Binary flag for employee departure | 1 (Yes, departed), 0 (No, active) | Facilitates DAX and SQL aggregations | `0` |
| **`IsActive`** | INT | int64 | Binary flag for active employee | 1 (No attrition), 0 (Departed) | Active headcount filtering | `1` |

---

## 3. Assumptions, Limitations & Boundary Constraints

1. **Denominator Consistency:** Across all queries and reports, the overall attrition rate denominator is defined as total employee population ($N = 326$) in the observed cohort.
2. **Observational Nature:** All relationships documented (e.g. between Overtime and Attrition) represent measured statistical associations and should not be construed as proven causal mechanisms without controlled interventions.
3. **Data Integrity Constraints:** The dataset satisfies strict relational integrity:
   - `YearsAtCompany <= YearsOfExperience`
   - `PromotionHistory <= YearsAtCompany`
   - `Salary > 0`
   - `AttendanceRate + (AbsenceDays / 250 * 100) = 100%`
   - `AttritionNumeric + IsActive = 1`
