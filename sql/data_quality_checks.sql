-- ============================================================================
-- HR Analytics: Data Quality & Integrity Validation Script
-- Dialect: PostgreSQL / ANSI SQL
-- Description: Comprehensive test suite to validate data cleanliness, identify
--              duplicates, verify null constraints, check logical consistency,
--              and detect boundary violations.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. Total Record Count and Basic Overview
-- ----------------------------------------------------------------------------
SELECT 
    COUNT(*) AS total_records,
    COUNT(DISTINCT employee_id) AS distinct_employees,
    COUNT(*) - COUNT(DISTINCT employee_id) AS duplicate_employee_ids
FROM hr_employees;

-- ----------------------------------------------------------------------------
-- 2. Duplicate Detection
-- Identifies any duplicate records based on primary identifier or full profile
-- ----------------------------------------------------------------------------
SELECT 
    employee_id,
    COUNT(*) AS appearance_count
FROM hr_employees
GROUP BY employee_id
HAVING COUNT(*) > 1;

-- ----------------------------------------------------------------------------
-- 3. Null & Missing Value Auditing Across Critical Fields
-- ----------------------------------------------------------------------------
SELECT
    COUNT(*) - COUNT(employee_id) AS missing_employee_ids,
    COUNT(*) - COUNT(age) AS missing_age,
    COUNT(*) - COUNT(department) AS missing_department,
    COUNT(*) - COUNT(job_role) AS missing_job_role,
    COUNT(*) - COUNT(salary) AS missing_salary,
    COUNT(*) - COUNT(years_of_experience) AS missing_experience,
    COUNT(*) - COUNT(years_at_company) AS missing_tenure,
    COUNT(*) - COUNT(attrition) AS missing_attrition,
    COUNT(*) - COUNT(attendance_rate) AS missing_attendance,
    COUNT(*) - COUNT(overtime) AS missing_overtime,
    COUNT(*) - COUNT(job_satisfaction) AS missing_job_satisfaction,
    COUNT(*) - COUNT(performance_rating) AS missing_performance_rating
FROM hr_employees;

-- ----------------------------------------------------------------------------
-- 4. Categorical Domain and Inconsistent Value Checks
-- ----------------------------------------------------------------------------
-- Validate Attrition domain ('Yes', 'No')
SELECT DISTINCT attrition, COUNT(*) AS count
FROM hr_employees
GROUP BY attrition;

-- Validate Overtime domain ('Yes', 'No')
SELECT DISTINCT overtime, COUNT(*) AS count
FROM hr_employees
GROUP BY overtime;

-- Validate Gender domain
SELECT DISTINCT gender, COUNT(*) AS count
FROM hr_employees
GROUP BY gender;

-- Validate Department domain
SELECT DISTINCT department, COUNT(*) AS count
FROM hr_employees
GROUP BY department;

-- ----------------------------------------------------------------------------
-- 5. Range & Boundary Sanity Checks
-- ----------------------------------------------------------------------------
SELECT
    MIN(age) AS min_age,
    MAX(age) AS max_age,
    MIN(salary) AS min_salary,
    MAX(salary) AS max_salary,
    MIN(attendance_rate) AS min_attendance_rate,
    MAX(attendance_rate) AS max_attendance_rate,
    MIN(absence_days) AS min_absence_days,
    MAX(absence_days) AS max_absence_days,
    MIN(job_satisfaction) AS min_job_satisfaction,
    MAX(job_satisfaction) AS max_job_satisfaction,
    MIN(performance_rating) AS min_performance_rating,
    MAX(performance_rating) AS max_performance_rating
FROM hr_employees;

-- ----------------------------------------------------------------------------
-- 6. Logical Consistency & Cross-Field Validations
-- ----------------------------------------------------------------------------
-- Check 1: Tenure at company cannot exceed total working years
SELECT 
    employee_id,
    age,
    years_of_experience,
    years_at_company
FROM hr_employees
WHERE years_at_company > years_of_experience;

-- Check 2: Promotion history cannot exceed tenure at company
SELECT 
    employee_id,
    years_at_company,
    promotion_history
FROM hr_employees
WHERE promotion_history > years_at_company;

-- Check 3: Attrition flags logical agreement: (attrition_numeric + is_active = 1)
SELECT 
    employee_id,
    attrition,
    attrition_numeric,
    is_active
FROM hr_employees
WHERE (attrition = 'Yes' AND (attrition_numeric <> 1 OR is_active <> 0))
   OR (attrition = 'No' AND (attrition_numeric <> 0 OR is_active <> 1));

-- Check 4: Age vs Total Working Years sanity (age - experience >= 14)
SELECT 
    employee_id,
    age,
    years_of_experience,
    (age - years_of_experience) AS implied_entry_age
FROM hr_employees
WHERE (age - years_of_experience) < 14;

-- Summary of Data Quality Status:
-- A clean dataset will yield 0 rows for all anomaly/consistency checks above.
