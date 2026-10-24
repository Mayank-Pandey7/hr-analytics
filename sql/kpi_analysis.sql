-- ============================================================================
-- HR Analytics: Executive KPI Analysis Script
-- Dialect: PostgreSQL / ANSI SQL
-- Description: Computes core organization-wide Human Resources KPIs, historical
--              attrition metrics, workforce tenure, compensation benchmarks,
--              overtime exposure, and attendance averages.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- KPI 1: Organization-Wide Executive KPI Summary Card
-- Denominator consistency: Total workforce (N = Total Employees)
-- ----------------------------------------------------------------------------
WITH ExecutiveKPIs AS (
    SELECT
        COUNT(*) AS total_employees,
        SUM(CASE WHEN attrition = 'No' THEN 1 ELSE 0 END) AS active_employees,
        SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS employees_who_left,
        ROUND((SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) / COUNT(*)) * 100, 2) AS overall_attrition_rate_pct,
        ROUND(AVG(salary), 2) AS avg_monthly_salary,
        ROUND(AVG(annual_salary), 2) AS avg_annual_salary,
        ROUND(AVG(years_of_experience), 2) AS avg_years_of_experience,
        ROUND(AVG(years_at_company), 2) AS avg_employee_tenure,
        ROUND(AVG(job_satisfaction), 2) AS avg_job_satisfaction,
        ROUND(AVG(performance_rating), 2) AS avg_performance_rating,
        ROUND((SUM(CASE WHEN overtime = 'Yes' THEN 1.0 ELSE 0 END) / COUNT(*)) * 100, 2) AS overtime_pct,
        ROUND((SUM(CASE WHEN promotion_in_last_3_years = 'Yes' THEN 1.0 ELSE 0 END) / COUNT(*)) * 100, 2) AS promotion_rate_last_3yrs_pct,
        ROUND(AVG(attendance_rate), 2) AS avg_attendance_rate_pct,
        ROUND(AVG(absence_days), 2) AS avg_absence_days
    FROM hr_employees
)
SELECT 
    total_employees,
    active_employees,
    employees_who_left,
    overall_attrition_rate_pct,
    avg_monthly_salary,
    avg_annual_salary,
    avg_years_of_experience,
    avg_employee_tenure,
    avg_job_satisfaction,
    avg_performance_rating,
    overtime_pct,
    promotion_rate_last_3yrs_pct,
    avg_attendance_rate_pct,
    avg_absence_days
FROM ExecutiveKPIs;

-- ----------------------------------------------------------------------------
-- KPI 2: Active vs Exited Employee Profile Comparison
-- Highlights divergence between employees who left vs retained talent
-- ----------------------------------------------------------------------------
SELECT 
    attrition,
    COUNT(*) AS headcount,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS cohort_pct,
    ROUND(AVG(age), 1) AS avg_age,
    ROUND(AVG(salary), 2) AS avg_monthly_salary,
    ROUND(AVG(years_of_experience), 1) AS avg_total_experience,
    ROUND(AVG(years_at_company), 1) AS avg_tenure_at_company,
    ROUND(AVG(job_satisfaction), 2) AS avg_job_satisfaction,
    ROUND(AVG(work_life_balance), 2) AS avg_work_life_balance,
    ROUND(AVG(attendance_rate), 2) AS avg_attendance_rate,
    ROUND(AVG(absence_days), 1) AS avg_absence_days,
    ROUND(SUM(CASE WHEN overtime = 'Yes' THEN 1.0 ELSE 0 END) * 100.0 / COUNT(*), 2) AS overtime_rate_pct
FROM hr_employees
GROUP BY attrition
ORDER BY attrition DESC;

-- ----------------------------------------------------------------------------
-- KPI 3: Promotion Rate & Tenure Segment Window Analysis
-- Analyzes promotion velocity across tenure quintiles
-- ----------------------------------------------------------------------------
WITH TenureQuintiles AS (
    SELECT 
        employee_id,
        years_at_company,
        promotion_history,
        promotion_in_last_3_years,
        attrition,
        NTILE(4) OVER (ORDER BY years_at_company) AS tenure_quartile
    FROM hr_employees
)
SELECT 
    tenure_quartile,
    MIN(years_at_company) AS min_tenure,
    MAX(years_at_company) AS max_tenure,
    COUNT(*) AS total_staff,
    SUM(CASE WHEN promotion_in_last_3_years = 'Yes' THEN 1 ELSE 0 END) AS promoted_last_3yrs,
    ROUND(SUM(CASE WHEN promotion_in_last_3_years = 'Yes' THEN 1.0 ELSE 0 END) * 100.0 / COUNT(*), 2) AS promotion_rate_pct,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate_pct
FROM TenureQuintiles
GROUP BY tenure_quartile
ORDER BY tenure_quartile;
