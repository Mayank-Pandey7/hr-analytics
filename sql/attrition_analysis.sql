-- ============================================================================
-- HR Analytics: In-Depth Attrition Driver & Risk Segment Analysis
-- Dialect: PostgreSQL / ANSI SQL
-- Description: Analyzes employee attrition rates across salary bands, experience,
--              overtime exposure, job satisfaction, work-life balance, tenure,
--              and demographic cohorts.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. Attrition by Overtime Status (The Primary Operational Workload Driver)
-- ----------------------------------------------------------------------------
SELECT 
    overtime,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate_pct,
    ROUND(AVG(salary), 2) AS avg_salary,
    ROUND(AVG(job_satisfaction), 2) AS avg_job_satisfaction,
    ROUND(AVG(work_life_balance), 2) AS avg_work_life_balance,
    ROUND(AVG(absence_days), 1) AS avg_absence_days
FROM hr_employees
GROUP BY overtime
ORDER BY attrition_rate_pct DESC;

-- ----------------------------------------------------------------------------
-- 2. Attrition by Monthly Salary Band
-- ----------------------------------------------------------------------------
SELECT 
    salary_band,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate_pct,
    ROUND(AVG(salary), 2) AS avg_salary_in_band,
    ROUND(AVG(years_at_company), 1) AS avg_tenure
FROM hr_employees
GROUP BY salary_band
ORDER BY MIN(salary) ASC;

-- ----------------------------------------------------------------------------
-- 3. Attrition by Experience Band (Career Stage)
-- ----------------------------------------------------------------------------
SELECT 
    experience_band,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate_pct,
    ROUND(AVG(salary), 2) AS avg_salary,
    ROUND(AVG(years_at_company), 1) AS avg_tenure
FROM hr_employees
GROUP BY experience_band
ORDER BY MIN(years_of_experience) ASC;

-- ----------------------------------------------------------------------------
-- 4. Attrition Cross-Tabulation: Job Satisfaction vs Work-Life Balance
-- Multi-dimensional risk matrix
-- ----------------------------------------------------------------------------
SELECT 
    job_satisfaction_label,
    work_life_balance_label,
    COUNT(*) AS total_staff,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate_pct
FROM hr_employees
GROUP BY job_satisfaction_label, work_life_balance_label
ORDER BY job_satisfaction_label, work_life_balance_label;

-- ----------------------------------------------------------------------------
-- 5. Attrition by Company Tenure Band & Promotion Recency
-- Detects career stagnation and early-career 'flight risk'
-- ----------------------------------------------------------------------------
SELECT 
    tenure_band,
    promotion_in_last_3_years,
    COUNT(*) AS employee_count,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate_pct,
    ROUND(AVG(salary), 2) AS avg_salary
FROM hr_employees
GROUP BY tenure_band, promotion_in_last_3_years
ORDER BY tenure_band, promotion_in_last_3_years DESC;

-- ----------------------------------------------------------------------------
-- 6. Attrition by Demographic Cohorts (Age Group & Marital Status)
-- ----------------------------------------------------------------------------
SELECT 
    age_group,
    marital_status,
    COUNT(*) AS employee_count,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate_pct,
    ROUND(AVG(salary), 2) AS avg_salary,
    ROUND(AVG(years_at_company), 1) AS avg_tenure
FROM hr_employees
GROUP BY age_group, marital_status
ORDER BY age_group, marital_status;

-- ----------------------------------------------------------------------------
-- 7. High-Risk Segment Identification CTE
-- Identifies employees combining multiple high-attrition risk factors:
-- (Overtime = 'Yes' AND JobSatisfaction <= 2 AND Salary < 5000)
-- ----------------------------------------------------------------------------
WITH EmployeeRiskProfile AS (
    SELECT
        employee_id,
        department,
        job_role,
        salary,
        overtime,
        job_satisfaction,
        work_life_balance,
        years_at_company,
        attrition,
        CASE 
            WHEN overtime = 'Yes' AND job_satisfaction <= 2 AND salary < 5000 THEN 'Critical Risk Segment'
            WHEN overtime = 'Yes' OR job_satisfaction <= 2 OR salary < 5000 THEN 'Moderate Risk'
            ELSE 'Low Risk'
        END AS risk_tier
    FROM hr_employees
)
SELECT 
    risk_tier,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate_pct,
    ROUND(AVG(salary), 2) AS avg_salary
FROM EmployeeRiskProfile
GROUP BY risk_tier
ORDER BY attrition_rate_pct DESC;
