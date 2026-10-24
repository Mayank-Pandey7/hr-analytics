"""
HR Analytics & Employee Attrition Statistical Analysis Runner
Executes SQL queries, computes key performance indicators (KPIs), performs statistical tests,
and exports reporting tables for Power BI and executive review.
"""

import os
import sqlite3
import pandas as pd
import numpy as np
from scipy import stats

def run_analysis(data_path='data/processed/fact_hr_analytics.csv',
                 output_dir='outputs/reports'):
    os.makedirs(output_dir, exist_ok=True)
    print(f"Loading processed dataset from {data_path}...")
    df = pd.read_csv(data_path)

    # 1. Standardize column names to exact ANSI SQL / PostgreSQL schema names
    col_mapping = {
        'EmployeeID': 'employee_id',
        'Age': 'age',
        'Gender': 'gender',
        'Department': 'department',
        'JobRole': 'job_role',
        'Salary': 'salary',
        'AnnualSalary': 'annual_salary',
        'YearsOfExperience': 'years_of_experience',
        'YearsAtCompany': 'years_at_company',
        'AttendanceRate': 'attendance_rate',
        'AbsenceDays': 'absence_days',
        'Overtime': 'overtime',
        'JobSatisfaction': 'job_satisfaction',
        'PerformanceRating': 'performance_rating',
        'PromotionHistory': 'promotion_history',
        'PromotionInLast3Years': 'promotion_in_last_3_years',
        'WorkLifeBalance': 'work_life_balance',
        'TrainingHours': 'training_hours',
        'Attrition': 'attrition',
        'AttritionNumeric': 'attrition_numeric',
        'IsActive': 'is_active',
        'AgeGroup': 'age_group',
        'SalaryBand': 'salary_band',
        'ExperienceBand': 'experience_band',
        'TenureBand': 'tenure_band',
        'JobSatisfactionLabel': 'job_satisfaction_label',
        'WorkLifeBalanceLabel': 'work_life_balance_label',
        'PerformanceRatingLabel': 'performance_rating_label',
        'MaritalStatus': 'marital_status',
        'EducationField': 'education_field',
        'BusinessTravel': 'business_travel'
    }

    df_sql = df.rename(columns=col_mapping)
    conn = sqlite3.connect(':memory:')
    df_sql.to_sql('hr_employees', conn, index=False, if_exists='replace')
    print("Loaded hr_employees table into SQL engine.")

    # 2. Executive KPI Calculation (KPI 1)
    kpi_query = """
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
        ROUND((SUM(CASE WHEN promotion_in_last_3_years = 'Yes' THEN 1.0 ELSE 0 END) / COUNT(*)) * 100, 2) AS promotion_rate_pct,
        ROUND(AVG(attendance_rate), 2) AS avg_attendance_rate_pct,
        ROUND(AVG(absence_days), 2) AS avg_absence_days
    FROM hr_employees;
    """
    kpis = pd.read_sql_query(kpi_query, conn)
    kpis.to_csv(os.path.join(output_dir, 'kpi_summary.csv'), index=False)
    print("\n=== EXECUTIVE HR KPIS ===")
    for col in kpis.columns:
        print(f"  {col}: {kpis[col].iloc[0]}")

    # 3. Departmental Analysis Query
    dept_query = """
    SELECT 
        department,
        COUNT(*) AS total_headcount,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM hr_employees), 2) AS pct_of_workforce,
        SUM(CASE WHEN attrition = 'No' THEN 1 ELSE 0 END) AS active_headcount,
        SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS departed_headcount,
        ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate_pct,
        ROUND(AVG(salary), 2) AS avg_monthly_salary,
        ROUND(AVG(performance_rating), 2) AS avg_performance_rating,
        ROUND(AVG(attendance_rate), 2) AS avg_attendance_rate_pct,
        ROUND(AVG(absence_days), 1) AS avg_absence_days
    FROM hr_employees
    GROUP BY department
    ORDER BY attrition_rate_pct DESC;
    """
    dept_df = pd.read_sql_query(dept_query, conn)
    dept_df.to_csv(os.path.join(output_dir, 'department_metrics.csv'), index=False)
    print("\n=== DEPARTMENTAL METRICS ===")
    print(dept_df.to_string(index=False))

    # 4. Job Role Breakdown
    role_query = """
    SELECT 
        department,
        job_role,
        COUNT(*) AS role_headcount,
        SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS departed_count,
        ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate_pct,
        ROUND(AVG(salary), 2) AS avg_monthly_salary,
        ROUND(AVG(years_at_company), 1) AS avg_tenure
    FROM hr_employees
    GROUP BY department, job_role
    ORDER BY attrition_rate_pct DESC;
    """
    role_df = pd.read_sql_query(role_query, conn)
    role_df.to_csv(os.path.join(output_dir, 'job_role_metrics.csv'), index=False)

    # 5. Overtime Analysis
    ot_query = """
    SELECT 
        overtime,
        COUNT(*) AS headcount,
        SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS departed_count,
        ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate_pct,
        ROUND(AVG(salary), 2) AS avg_salary,
        ROUND(AVG(job_satisfaction), 2) AS avg_job_satisfaction,
        ROUND(AVG(work_life_balance), 2) AS avg_work_life_balance,
        ROUND(AVG(absence_days), 1) AS avg_absence_days
    FROM hr_employees
    GROUP BY overtime;
    """
    ot_df = pd.read_sql_query(ot_query, conn)
    ot_df.to_csv(os.path.join(output_dir, 'attrition_by_overtime.csv'), index=False)

    # 6. Salary Band Analysis
    sal_query = """
    SELECT 
        salary_band,
        COUNT(*) AS total_employees,
        SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
        ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate_pct,
        ROUND(AVG(salary), 2) AS avg_salary,
        ROUND(AVG(years_at_company), 1) AS avg_tenure
    FROM hr_employees
    GROUP BY salary_band
    ORDER BY MIN(salary) ASC;
    """
    sal_df = pd.read_sql_query(sal_query, conn)
    sal_df.to_csv(os.path.join(output_dir, 'attrition_by_salary_band.csv'), index=False)

    # 7. Experience Band Analysis
    exp_query = """
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
    """
    exp_df = pd.read_sql_query(exp_query, conn)
    exp_df.to_csv(os.path.join(output_dir, 'attrition_by_experience.csv'), index=False)

    # 8. High-Risk Multi-Factor Segment Analysis
    risk_query = """
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
    """
    risk_df = pd.read_sql_query(risk_query, conn)
    risk_df.to_csv(os.path.join(output_dir, 'attrition_risk_matrix.csv'), index=False)
    print("\n=== MULTI-FACTOR ATTRITION RISK TIERS ===")
    print(risk_df.to_string(index=False))

    # 9. Statistical Significance Tests
    print("\n=== STATISTICAL HYPOTHESIS TESTING ===")
    # 9a. Salary: Attrition Yes vs No (Mann-Whitney U Test)
    sal_yes = df[df['Attrition'] == 'Yes']['Salary']
    sal_no = df[df['Attrition'] == 'No']['Salary']
    u_stat, u_pval = stats.mannwhitneyu(sal_yes, sal_no, alternative='two-sided')
    print(f"1. Salary comparison (Attrition Yes vs No):")
    print(f"   Median Salary (Yes): ${sal_yes.median():,.2f} | (No): ${sal_no.median():,.2f}")
    print(f"   Mann-Whitney U p-value: {u_pval:.4e} ({'Statistically Significant (p < 0.05)' if u_pval < 0.05 else 'Not Significant'})")

    # 9b. Overtime vs Attrition (Chi-Square Contingency Test)
    ot_crosstab = pd.crosstab(df['Overtime'], df['Attrition'])
    chi2, chi_pval, dof, _ = stats.chi2_contingency(ot_crosstab)
    print(f"\n2. Overtime vs Attrition Chi-Square Test:")
    print(f"   Chi2: {chi2:.2f}, dof: {dof}, p-value: {chi_pval:.4e} ({'Statistically Significant' if chi_pval < 0.05 else 'Not Significant'})")

    # 9c. Job Satisfaction vs Attrition (Chi-Square)
    sat_crosstab = pd.crosstab(df['JobSatisfaction'], df['Attrition'])
    chi2_sat, pval_sat, _, _ = stats.chi2_contingency(sat_crosstab)
    print(f"\n3. Job Satisfaction vs Attrition Chi-Square Test:")
    print(f"   Chi2: {chi2_sat:.2f}, p-value: {pval_sat:.4e} ({'Statistically Significant' if pval_sat < 0.05 else 'Not Significant'})")

    # Save summary report
    stat_summary = pd.DataFrame([
        {'Test': 'Salary (Mann-Whitney U)', 'Stat': round(u_stat, 2), 'p_value': u_pval, 'Significant': u_pval < 0.05},
        {'Test': 'Overtime (Chi-Square)', 'Stat': round(chi2, 2), 'p_value': chi_pval, 'Significant': chi_pval < 0.05},
        {'Test': 'Job Satisfaction (Chi-Square)', 'Stat': round(chi2_sat, 2), 'p_value': pval_sat, 'Significant': pval_sat < 0.05}
    ])
    stat_summary.to_csv(os.path.join(output_dir, 'statistical_tests.csv'), index=False)

    conn.close()
    print(f"\nAll analysis reports exported successfully to {output_dir}")

if __name__ == '__main__':
    run_analysis()
