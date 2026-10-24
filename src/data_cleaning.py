"""
HR Analytics Data Cleaning and Transformation Module
Transforms raw HR employee data into standardized, clean, Power BI & SQL ready tables.
"""

import os
import pandas as pd
import numpy as np

def clean_and_transform_hr_data(raw_path='data/raw/hr_employee_data_raw.csv',
                                processed_path='data/processed/hr_employee_data_clean.csv',
                                seed=42):
    np.random.seed(seed)
    print(f"Loading raw dataset from {raw_path}...")
    df = pd.read_csv(raw_path)

    initial_rows, initial_cols = df.shape
    print(f"Raw shape: {initial_rows} rows, {initial_cols} columns")

    # 1. Clean string values & whitespace
    str_cols = df.select_dtypes(include=['object', 'string']).columns
    for col in str_cols:
        df[col] = df[col].astype(str).str.strip()

    # Normalize TravelRarely typo if present
    if 'BusinessTravel' in df.columns:
        df['BusinessTravel'] = df['BusinessTravel'].replace({'TravelRarely': 'Travel_Rarely'})

    # 2. Standardize Column Names to prompt specifications
    col_mapping = {
        'EmpID': 'EmployeeID',
        'MonthlyIncome': 'Salary',
        'TotalWorkingYears': 'YearsOfExperience',
        'OverTime': 'Overtime',
        'YearsSinceLastPromotion': 'PromotionHistory'
    }
    df = df.rename(columns=col_mapping)

    # 3. Handle Missing Values / Deduplication
    dup_emp_count = df.duplicated(subset=['EmployeeID']).sum()
    if dup_emp_count > 0:
        print(f"Found {dup_emp_count} duplicate EmployeeIDs. Deduplicating...")
        df = df.drop_duplicates(subset=['EmployeeID'], keep='first')

    # Ensure required numeric fields have no nulls and correct types
    df['EmployeeID'] = df['EmployeeID'].astype(str)
    df['Age'] = df['Age'].astype(int)
    df['Salary'] = df['Salary'].astype(int)
    df['MonthlyIncome'] = df['Salary'] # keep both for clarity
    df['AnnualSalary'] = df['Salary'] * 12
    df['YearsOfExperience'] = df['YearsOfExperience'].astype(int)
    df['YearsAtCompany'] = df['YearsAtCompany'].astype(int)
    df['JobSatisfaction'] = df['JobSatisfaction'].astype(int)
    df['PerformanceRating'] = df['PerformanceRating'].astype(int)
    df['PromotionHistory'] = df['PromotionHistory'].astype(int)
    df['WorkLifeBalance'] = df['WorkLifeBalance'].astype(int)
    
    # 4. Synthesize realistic AttendanceRate, AbsenceDays, and TrainingHours if missing
    if 'AbsenceDays' not in df.columns:
        # Realistic corporate absenteeism model (benchmark working days = 250/yr)
        env_sat = df['EnvironmentSatisfaction'].fillna(3) if 'EnvironmentSatisfaction' in df.columns else 3
        job_sat = df['JobSatisfaction']
        wlb = df['WorkLifeBalance']
        ot_penalty = (df['Overtime'] == 'Yes').astype(int) * 2
        
        # Base absence inversely proportional to satisfaction and balance
        base_absence = 14 - (0.8 * env_sat + 0.8 * job_sat + 0.9 * wlb) + ot_penalty
        noise = np.random.poisson(lam=2, size=len(df))
        absence_days = np.clip(np.round(base_absence + noise), 0, 24).astype(int)
        df['AbsenceDays'] = absence_days
        
    if 'AttendanceRate' not in df.columns:
        df['AttendanceRate'] = np.round(((250 - df['AbsenceDays']) / 250) * 100, 2)
        
    if 'TrainingHours' not in df.columns:
        if 'TrainingTimesLastYear' in df.columns:
            training_noise = np.random.randint(-2, 4, size=len(df))
            df['TrainingHours'] = np.clip(df['TrainingTimesLastYear'] * 12 + training_noise, 8, 80).astype(int)
        else:
            df['TrainingHours'] = np.random.randint(12, 60, size=len(df))

    # 5. Core KPI and Analytical Flag Engineering
    df['AttritionNumeric'] = (df['Attrition'] == 'Yes').astype(int)
    df['IsActive'] = (df['Attrition'] == 'No').astype(int)
    df['PromotionInLast3Years'] = np.where(df['PromotionHistory'] <= 3, 'Yes', 'No')

    # Categorical Bins
    # Age Group
    age_bins = [0, 24, 34, 44, 54, 120]
    age_labels = ['<25', '25-34', '35-44', '45-54', '55+']
    df['AgeGroup'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels, right=True).astype(str)

    # Salary Band (Monthly)
    sal_bins = [0, 3499, 6999, 11999, 1000000]
    sal_labels = ['< $3,500 (Entry)', '$3,500 - $6,999 (Mid)', '$7,000 - $11,999 (Senior)', '$12,000+ (Executive)']
    df['SalaryBand'] = pd.cut(df['Salary'], bins=sal_bins, labels=sal_labels, right=True).astype(str)

    # Experience Band
    exp_bins = [-1, 2, 5, 10, 20, 100]
    exp_labels = ['0-2 Years', '3-5 Years', '6-10 Years', '11-20 Years', '20+ Years']
    df['ExperienceBand'] = pd.cut(df['YearsOfExperience'], bins=exp_bins, labels=exp_labels, right=True).astype(str)

    # Tenure Band
    tenure_bins = [-1, 1, 2, 5, 10, 100]
    tenure_labels = ['< 1 Year', '1-2 Years', '3-5 Years', '6-10 Years', '10+ Years']
    df['TenureBand'] = pd.cut(df['YearsAtCompany'], bins=tenure_bins, labels=tenure_labels, right=True).astype(str)

    # Likert Scale Labels for Reporting
    sat_map = {1: '1 - Low', 2: '2 - Medium', 3: '3 - High', 4: '4 - Very High'}
    df['JobSatisfactionLabel'] = df['JobSatisfaction'].map(sat_map)

    wlb_map = {1: '1 - Bad', 2: '2 - Good', 3: '3 - Better', 4: '4 - Best'}
    df['WorkLifeBalanceLabel'] = df['WorkLifeBalance'].map(wlb_map)

    perf_map = {1: '1 - Low', 2: '2 - Good', 3: '3 - Excellent', 4: '4 - Outstanding'}
    df['PerformanceRatingLabel'] = df['PerformanceRating'].map(perf_map)

    # 6. Save processed clean dataset
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    df.to_csv(processed_path, index=False)
    print(f"Cleaned dataset saved successfully to {processed_path}")
    print(f"Final clean shape: {df.shape[0]} rows, {df.shape[1]} columns")

    # 7. Export Power BI ready dimension and summary tables
    export_star_schema_tables(df, os.path.dirname(processed_path))

    return df

def export_star_schema_tables(df, output_dir='data/processed'):
    # Fact Table: fact_hr_analytics.csv
    fact_cols = [
        'EmployeeID', 'Age', 'Gender', 'Department', 'JobRole', 'Salary', 'AnnualSalary',
        'YearsOfExperience', 'YearsAtCompany', 'AttendanceRate', 'AbsenceDays', 'Overtime',
        'JobSatisfaction', 'PerformanceRating', 'PromotionHistory', 'PromotionInLast3Years',
        'WorkLifeBalance', 'TrainingHours', 'Attrition', 'AttritionNumeric', 'IsActive',
        'AgeGroup', 'SalaryBand', 'ExperienceBand', 'TenureBand',
        'JobSatisfactionLabel', 'WorkLifeBalanceLabel', 'PerformanceRatingLabel',
        'MaritalStatus', 'EducationField', 'BusinessTravel'
    ]
    # Filter to existing cols
    fact_cols = [c for c in fact_cols if c in df.columns]
    df[fact_cols].to_csv(os.path.join(output_dir, 'fact_hr_analytics.csv'), index=False)

    # Dimension 1: dim_department.csv
    dim_dept = df[['Department']].drop_duplicates().sort_values('Department').reset_index(drop=True)
    dim_dept['DepartmentID'] = range(1, len(dim_dept) + 1)
    dim_dept.to_csv(os.path.join(output_dir, 'dim_department.csv'), index=False)

    # Dimension 2: dim_job_role.csv
    dim_role = df[['Department', 'JobRole']].drop_duplicates().sort_values(['Department', 'JobRole']).reset_index(drop=True)
    dim_role['JobRoleID'] = range(1, len(dim_role) + 1)
    dim_role.to_csv(os.path.join(output_dir, 'dim_job_role.csv'), index=False)

    # Dimension 3: dim_demographics.csv
    dim_demo = df[['AgeGroup']].drop_duplicates().sort_values('AgeGroup').reset_index(drop=True)
    dim_demo.to_csv(os.path.join(output_dir, 'dim_age_group.csv'), index=False)

    # Dimension 4: dim_satisfaction.csv
    dim_sat = pd.DataFrame({
        'JobSatisfaction': [1, 2, 3, 4],
        'JobSatisfactionLabel': ['1 - Low', '2 - Medium', '3 - High', '4 - Very High'],
        'SatisfactionCategory': ['Dissatisfied', 'Neutral', 'Satisfied', 'Highly Satisfied']
    })
    dim_sat.to_csv(os.path.join(output_dir, 'dim_satisfaction.csv'), index=False)

    print(f"Exported Star Schema tables to {output_dir}")

if __name__ == '__main__':
    clean_and_transform_hr_data()
