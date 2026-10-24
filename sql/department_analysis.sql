-- ============================================================================
-- HR Analytics: Department & Job Role Deep-Dive Analysis
-- Dialect: PostgreSQL / ANSI SQL
-- Description: Examines workforce distribution, departmental attrition rates,
--              compensation structures, performance benchmarks, and absenteeism
--              using CTEs, Window Functions, and multi-level aggregations.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. Departmental Headcount, Attrition Rate & Compensation Summary
-- ----------------------------------------------------------------------------
SELECT 
    department,
    COUNT(*) AS total_headcount,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS pct_of_total_workforce,
    SUM(CASE WHEN attrition = 'No' THEN 1 ELSE 0 END) AS active_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS departed_employees,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) * 100.0 / COUNT(*), 2) AS dept_attrition_rate_pct,
    ROUND(AVG(salary), 2) AS avg_monthly_salary,
    ROUND(AVG(annual_salary), 2) AS avg_annual_salary,
    ROUND(AVG(performance_rating), 2) AS avg_performance_rating,
    ROUND(AVG(attendance_rate), 2) AS avg_attendance_rate_pct,
    ROUND(AVG(absence_days), 1) AS avg_absence_days
FROM hr_employees
GROUP BY department
ORDER BY dept_attrition_rate_pct DESC;

-- ----------------------------------------------------------------------------
-- 2. Department & Job Role Breakdown with Headcount & Compensation
-- ----------------------------------------------------------------------------
SELECT 
    department,
    job_role,
    COUNT(*) AS role_headcount,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS role_attrition_count,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) * 100.0 / COUNT(*), 2) AS role_attrition_rate_pct,
    ROUND(AVG(salary), 2) AS avg_monthly_salary,
    MIN(salary) AS min_monthly_salary,
    MAX(salary) AS max_monthly_salary,
    ROUND(AVG(years_at_company), 1) AS avg_company_tenure,
    ROUND(AVG(performance_rating), 2) AS avg_performance_rating
FROM hr_employees
GROUP BY department, job_role
ORDER BY department ASC, role_attrition_rate_pct DESC;

-- ----------------------------------------------------------------------------
-- 3. Window Function Analysis: Salary Benchmark vs Department Average
-- Calculates how each job role's average pay deviates from its department mean
-- ----------------------------------------------------------------------------
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

-- ----------------------------------------------------------------------------
-- 4. Attendance & Overtime Exposure by Department
-- ----------------------------------------------------------------------------
SELECT 
    department,
    COUNT(*) AS total_staff,
    SUM(CASE WHEN overtime = 'Yes' THEN 1 ELSE 0 END) AS overtime_workers,
    ROUND(SUM(CASE WHEN overtime = 'Yes' THEN 1.0 ELSE 0 END) * 100.0 / COUNT(*), 2) AS overtime_rate_pct,
    ROUND(AVG(attendance_rate), 2) AS avg_attendance_rate,
    ROUND(AVG(absence_days), 1) AS avg_absence_days,
    ROUND(AVG(CASE WHEN overtime = 'Yes' THEN absence_days ELSE NULL END), 1) AS avg_absence_ot_workers,
    ROUND(AVG(CASE WHEN overtime = 'No' THEN absence_days ELSE NULL END), 1) AS avg_absence_non_ot_workers
FROM hr_employees
GROUP BY department
ORDER BY overtime_rate_pct DESC;
