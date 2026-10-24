"""
HR Analytics Dataset Generator
Generates a realistic synthetic HR employee attrition dataset for data analysis,
SQL queries, Power BI reporting, and machine learning.
"""

import os
import random
import numpy as np
import pandas as pd

def generate_hr_dataset(num_records=1500, random_state=42):
    np.random.seed(random_state)
    random.seed(random_state)

    departments_roles = {
        'Sales': [
            ('Sales Executive', 0.55, 4500, 11000),
            ('Sales Representative', 0.35, 2200, 4800),
            ('Manager', 0.10, 12000, 20000)
        ],
        'Research & Development': [
            ('Research Scientist', 0.35, 3500, 9500),
            ('Laboratory Technician', 0.30, 2500, 5200),
            ('Manufacturing Director', 0.15, 6000, 13500),
            ('Healthcare Representative', 0.12, 5500, 12000),
            ('Research Director', 0.05, 13000, 19500),
            ('Manager', 0.03, 13000, 20000)
        ],
        'Human Resources': [
            ('Human Resources', 0.80, 2800, 8500),
            ('Manager', 0.20, 11500, 19000)
        ]
    }

    dept_weights = [0.30, 0.64, 0.06] # 30% Sales, 64% R&D, 6% HR
    dept_choices = ['Sales', 'Research & Development', 'Human Resources']

    records = []

    for i in range(1, num_records + 1):
        emp_id = f"EMP{i:04d}"
        
        # Department & Role
        dept = np.random.choice(dept_choices, p=dept_weights)
        role_info = departments_roles[dept]
        roles = [r[0] for r in role_info]
        r_weights = [r[1] for r in role_info]
        r_weights = [w / sum(r_weights) for w in r_weights]
        role = np.random.choice(roles, p=r_weights)
        
        salary_range = next(r[2:] for r in role_info if r[0] == role)

        # Age and Demographics
        if 'Manager' in role or 'Director' in role:
            age = int(np.clip(np.random.normal(44, 7), 28, 60))
        elif 'Representative' in role or 'Technician' in role:
            age = int(np.clip(np.random.normal(31, 6), 19, 52))
        else:
            age = int(np.clip(np.random.normal(36, 7), 22, 58))
            
        gender = np.random.choice(['Male', 'Female'], p=[0.58, 0.42])
        marital = np.random.choice(['Single', 'Married', 'Divorced'], p=[0.32, 0.46, 0.22])
        
        # Education
        if dept == 'Sales':
            edu_field = np.random.choice(['Marketing', 'Life Sciences', 'Medical', 'Other'], p=[0.50, 0.25, 0.15, 0.10])
        elif dept == 'Research & Development':
            edu_field = np.random.choice(['Life Sciences', 'Medical', 'Technical Degree', 'Other'], p=[0.45, 0.35, 0.15, 0.05])
        else:
            edu_field = np.random.choice(['Human Resources', 'Life Sciences', 'Medical', 'Other'], p=[0.60, 0.20, 0.10, 0.10])

        # Experience & Tenure
        max_exp = max(0, age - 18)
        years_exp = int(np.clip(np.random.exponential(scale=max_exp * 0.45), 0, max_exp))
        if 'Manager' in role or 'Director' in role:
            years_exp = max(years_exp, int(np.random.uniform(9, max_exp)))

        years_company = int(np.clip(np.random.exponential(scale=years_exp * 0.55), 0, years_exp))
        years_since_promotion = int(min(years_company, np.random.geometric(p=0.3) - 1))
        promotion_last_3yrs = 'Yes' if years_since_promotion <= 3 else 'No'

        # Salary based on experience and role base
        base_min, base_max = salary_range
        exp_factor = min(1.0, years_exp / 25.0)
        salary = int(base_min + (base_max - base_min) * (0.35 * exp_factor + 0.65 * np.random.beta(2, 2)))
        annual_salary = salary * 12

        # Overtime
        ot_prob = 0.38 if role in ['Sales Representative', 'Laboratory Technician'] else 0.24
        overtime = 'Yes' if np.random.rand() < ot_prob else 'No'

        # Attendance & Absence
        # Normal attendance rate around 95%, with standard deviation 4%
        attendance_base = np.random.normal(0.95, 0.04)
        if overtime == 'Yes':
            attendance_base -= 0.015
        attendance_rate = round(float(np.clip(attendance_base, 0.78, 1.0) * 100), 2)
        absence_days = int(round((100.0 - attendance_rate) * 0.9 + np.random.poisson(2)))

        # Satisfaction and Balance (1 to 4)
        # 1=Low, 2=Medium, 3=High, 4=Very High
        job_sat_p = [0.18, 0.22, 0.34, 0.26]
        if overtime == 'Yes':
            job_sat_p = [0.28, 0.28, 0.26, 0.18]
        job_sat = int(np.random.choice([1, 2, 3, 4], p=job_sat_p))

        work_life_p = [0.12, 0.25, 0.45, 0.18]
        if overtime == 'Yes':
            work_life_p = [0.28, 0.38, 0.24, 0.10]
        work_life = int(np.random.choice([1, 2, 3, 4], p=work_life_p))

        # Performance Rating (1=Low, 2=Good, 3=Excellent, 4=Outstanding)
        # Typical corporate rating distribution centered at 3
        perf_p = [0.03, 0.12, 0.70, 0.15]
        perf_rating = int(np.random.choice([1, 2, 3, 4], p=perf_p))

        training_hours = int(np.clip(np.random.normal(32, 12), 10, 65))

        # Attrition Log-Odds Model
        # Baseline log-odds adjusted for realistic benchmark attrition rate (~16-17%)
        logit = -3.25
        # Overtime effect
        if overtime == 'Yes':
            logit += 1.15
        # Low Job Satisfaction
        if job_sat == 1:
            logit += 1.10
        elif job_sat == 2:
            logit += 0.45
        elif job_sat == 4:
            logit -= 0.50
        # Work life balance
        if work_life == 1:
            logit += 0.95
        elif work_life == 4:
            logit -= 0.40
        # Low salary relative to median ($5000)
        if salary < 3500:
            logit += 0.85
        elif salary > 9000:
            logit -= 0.75
        # Role specific risk
        if role in ['Sales Representative', 'Laboratory Technician']:
            logit += 0.55
        elif role in ['Manager', 'Research Director']:
            logit -= 0.90
        # Lack of promotion (stagnation)
        if years_since_promotion >= 5 and years_company >= 5:
            logit += 0.65
        # High absence
        if absence_days > 12:
            logit += 0.45
        # Marital status (Singles tend to have higher mobility)
        if marital == 'Single':
            logit += 0.50
        # Early tenure risk (first 2 years)
        if years_company <= 2:
            logit += 0.60
        elif years_company >= 8:
            logit -= 0.40

        prob_attrition = 1.0 / (1.0 + np.exp(-logit))
        attrition = 'Yes' if np.random.rand() < prob_attrition else 'No'

        records.append({
            'EmployeeID': emp_id,
            'Age': age,
            'Gender': gender,
            'MaritalStatus': marital,
            'Department': dept,
            'JobRole': role,
            'EducationField': edu_field,
            'MonthlyIncome': salary,
            'AnnualSalary': annual_salary,
            'YearsOfExperience': years_exp,
            'YearsAtCompany': years_company,
            'AttendanceRate': attendance_rate,
            'AbsenceDays': absence_days,
            'Overtime': overtime,
            'JobSatisfaction': job_sat,
            'PerformanceRating': perf_rating,
            'PromotionHistory': years_since_promotion,
            'PromotionInLast3Years': promotion_last_3yrs,
            'WorkLifeBalance': work_life,
            'TrainingHours': training_hours,
            'Attrition': attrition
        })

    df = pd.DataFrame(records)
    return df

if __name__ == '__main__':
    output_raw = os.path.join('data', 'raw', 'hr_employee_data_raw.csv')
    os.makedirs(os.path.dirname(output_raw), exist_ok=True)
    df = generate_hr_dataset(num_records=1500, random_state=42)
    df.to_csv(output_raw, index=False)
    print(f"Generated {len(df)} records saved to {output_raw}")
    print(f"Overall Attrition Count: {df['Attrition'].value_counts().to_dict()}")
    print(f"Overall Attrition Rate: {df['Attrition'].value_counts(normalize=True)['Yes']*100:.2f}%")
