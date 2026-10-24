-- ============================================================================
-- HR Analytics & Employee Attrition Database Schema
-- Dialect: PostgreSQL (Compatible with MySQL 8.0+)
-- Description: DDL script to create the HR Analytics database, tables, constraints,
--              and indexes for analytical reporting and KPI calculation.
-- ============================================================================

-- Optional: Create Database
-- CREATE DATABASE hr_analytics;
-- \c hr_analytics;

-- Drop table if exists for idempotency
DROP TABLE IF EXISTS hr_employees CASCADE;

-- Create Main Table
CREATE TABLE hr_employees (
    employee_id             VARCHAR(20) PRIMARY KEY,
    age                     INT NOT NULL CHECK (age >= 18 AND age <= 100),
    gender                  VARCHAR(10) NOT NULL CHECK (gender IN ('Male', 'Female', 'Non-Binary', 'Other')),
    marital_status          VARCHAR(20) CHECK (marital_status IN ('Single', 'Married', 'Divorced')),
    department              VARCHAR(50) NOT NULL,
    job_role                VARCHAR(50) NOT NULL,
    education_field         VARCHAR(50),
    salary                  NUMERIC(10, 2) NOT NULL CHECK (salary >= 0),
    annual_salary           NUMERIC(12, 2) NOT NULL CHECK (annual_salary >= 0),
    years_of_experience     INT NOT NULL CHECK (years_of_experience >= 0),
    years_at_company        INT NOT NULL CHECK (years_at_company >= 0),
    attendance_rate         NUMERIC(5, 2) NOT NULL CHECK (attendance_rate >= 0 AND attendance_rate <= 100),
    absence_days            INT NOT NULL CHECK (absence_days >= 0),
    overtime                VARCHAR(5) NOT NULL CHECK (overtime IN ('Yes', 'No')),
    job_satisfaction        INT NOT NULL CHECK (job_satisfaction BETWEEN 1 AND 4),
    performance_rating      INT NOT NULL CHECK (performance_rating BETWEEN 1 AND 4),
    promotion_history       INT NOT NULL CHECK (promotion_history >= 0),
    promotion_in_last_3_years VARCHAR(5) CHECK (promotion_in_last_3_years IN ('Yes', 'No')),
    work_life_balance       INT NOT NULL CHECK (work_life_balance BETWEEN 1 AND 4),
    training_hours          INT NOT NULL CHECK (training_hours >= 0),
    attrition               VARCHAR(5) NOT NULL CHECK (attrition IN ('Yes', 'No')),
    attrition_numeric       INT NOT NULL CHECK (attrition_numeric IN (0, 1)),
    is_active               INT NOT NULL CHECK (is_active IN (0, 1)),
    age_group               VARCHAR(20),
    salary_band             VARCHAR(50),
    experience_band         VARCHAR(50),
    tenure_band             VARCHAR(50),
    job_satisfaction_label  VARCHAR(50),
    work_life_balance_label VARCHAR(50),
    performance_rating_label VARCHAR(50),
    business_travel         VARCHAR(50),
    created_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- Performance Indexes for Analytics Queries
-- ============================================================================
CREATE INDEX idx_hr_department ON hr_employees(department);
CREATE INDEX idx_hr_job_role ON hr_employees(job_role);
CREATE INDEX idx_hr_attrition ON hr_employees(attrition);
CREATE INDEX idx_hr_overtime ON hr_employees(overtime);
CREATE INDEX idx_hr_salary_band ON hr_employees(salary_band);
CREATE INDEX idx_hr_age_group ON hr_employees(age_group);
CREATE INDEX idx_hr_tenure_band ON hr_employees(tenure_band);

-- ============================================================================
-- Data Ingestion Instructions:
-- PostgreSQL:
-- \copy hr_employees(employee_id,age,gender,marital_status,department,job_role,education_field,salary,annual_salary,years_of_experience,years_at_company,attendance_rate,absence_days,overtime,job_satisfaction,performance_rating,promotion_history,promotion_in_last_3_years,work_life_balance,training_hours,attrition,attrition_numeric,is_active,age_group,salary_band,experience_band,tenure_band,job_satisfaction_label,work_life_balance_label,performance_rating_label,business_travel)
-- FROM '/path/to/data/processed/fact_hr_analytics.csv' WITH (FORMAT csv, HEADER true);
-- ============================================================================
