# Power BI DAX Measures Library: HR Analytics & Workforce Intelligence

Create a dedicated disconnected table named `_Measures` in Power BI Desktop to house all business metrics.

```dax
_Measures = ROW("Description", "Container table for all HR Analytics DAX Measures")
```

---

## 1. Headcount & Attrition KPIs

### 1.1 Total Employees
Calculates the total count of employee records in the current filter context.
```dax
Total Employees = 
COUNTROWS('fact_hr_analytics')
```
*Format: `#,##0` (Whole Number)*

### 1.2 Active Employees
Calculates headcount of currently employed staff (`Attrition = "No"`).
```dax
Active Employees = 
CALCULATE(
    COUNTROWS('fact_hr_analytics'),
    'fact_hr_analytics'[Attrition] = "No"
)
```
*Format: `#,##0` (Whole Number)*

### 1.3 Employees Who Left (Departed Headcount)
Calculates total employees who exited the organization (`Attrition = "Yes"`).
```dax
Employees Who Left = 
CALCULATE(
    COUNTROWS('fact_hr_analytics'),
    'fact_hr_analytics'[Attrition] = "Yes"
)
```
*Format: `#,##0` (Whole Number)*

### 1.4 Overall Attrition Rate (%)
The core executive KPI. Denominator is Total Employees in the filter context.
$$\text{Attrition Rate} = \frac{\text{Employees Who Left}}{\text{Total Employees}} \times 100$$
```dax
Attrition Rate % = 
DIVIDE(
    [Employees Who Left],
    [Total Employees],
    0
)
```
*Format: `0.0%` (Percentage)*

---

## 2. Compensation & Tenure KPIs

### 2.1 Average Monthly Salary
Calculates the mean base monthly income across filtered employees.
```dax
Avg Monthly Salary = 
AVERAGE('fact_hr_analytics'[Salary])
```
*Format: `$#,##0` (Currency)*

### 2.2 Average Annual Salary
Calculates mean annualized compensation.
```dax
Avg Annual Salary = 
AVERAGE('fact_hr_analytics'[AnnualSalary])
```
*Format: `$#,##0` (Currency)*

### 2.3 Average Company Tenure
Mean duration (in years) employees have been with the organization.
```dax
Avg Company Tenure = 
AVERAGE('fact_hr_analytics'[YearsAtCompany])
```
*Format: `0.0` (Decimal Number, 1 decimal place)*

### 2.4 Average Total Experience
Mean career experience across the workforce.
```dax
Avg Total Experience = 
AVERAGE('fact_hr_analytics'[YearsOfExperience])
```
*Format: `0.0` (Decimal Number)*

---

## 3. Operations, Performance & Attendance KPIs

### 3.1 Overtime Headcount
Number of employees engaged in mandatory or voluntary overtime.
```dax
Overtime Headcount = 
CALCULATE(
    COUNTROWS('fact_hr_analytics'),
    'fact_hr_analytics'[Overtime] = "Yes"
)
```
*Format: `#,##0`*

### 3.2 Overtime Percentage (%)
Proportion of workforce exposed to overtime demands.
```dax
Overtime % = 
DIVIDE(
    [Overtime Headcount],
    [Total Employees],
    0
)
```
*Format: `0.0%` (Percentage)*

### 3.3 Average Attendance Rate (%)
Workforce average attendance percentage.
```dax
Avg Attendance Rate % = 
AVERAGE('fact_hr_analytics'[AttendanceRate]) / 100
```
*Format: `0.0%` (Percentage)*

### 3.4 Average Absence Days
Average unscheduled or scheduled absenteeism in days per employee per year.
```dax
Avg Absence Days = 
AVERAGE('fact_hr_analytics'[AbsenceDays])
```
*Format: `0.0` (Decimal Number)*

### 3.5 Average Job Satisfaction (Likert 1-4)
Mean job satisfaction rating (1 = Low, 4 = Very High).
```dax
Avg Job Satisfaction = 
AVERAGE('fact_hr_analytics'[JobSatisfaction])
```
*Format: `0.00` (Decimal Number)*

### 3.6 Average Performance Rating (1-4)
Mean annual appraisal performance score.
```dax
Avg Performance Rating = 
AVERAGE('fact_hr_analytics'[PerformanceRating])
```
*Format: `0.00` (Decimal Number)*

### 3.7 Average Work-Life Balance (1-4)
Mean employee-reported work-life balance score.
```dax
Avg Work-Life Balance = 
AVERAGE('fact_hr_analytics'[WorkLifeBalance])
```
*Format: `0.00` (Decimal Number)*

### 3.8 Promotion Rate (Last 3 Years) (%)
Percentage of workforce that received a promotion within the last 3 years.
```dax
Promotion Rate Last 3 Yrs % = 
DIVIDE(
    CALCULATE(
        COUNTROWS('fact_hr_analytics'),
        'fact_hr_analytics'[PromotionInLast3Years] = "Yes"
    ),
    [Total Employees],
    0
)
```
*Format: `0.0%` (Percentage)*

---

## 4. Risk Segmentation & Conditional Formatting Measures

### 4.1 Critical Risk Headcount
Employees flagged under all three primary risk drivers: Overtime = Yes, Satisfaction <= 2, Salary < $5,000.
```dax
Critical Risk Headcount = 
CALCULATE(
    COUNTROWS('fact_hr_analytics'),
    'fact_hr_analytics'[Overtime] = "Yes",
    'fact_hr_analytics'[JobSatisfaction] <= 2,
    'fact_hr_analytics'[Salary] < 5000
)
```
*Format: `#,##0`*

### 4.2 Attrition Rate KPI Conditional Color
Dynamic hex code measure for visual KPI alerts and KPI card font colors.
```dax
Attrition KPI Color = 
SWITCH(
    TRUE(),
    [Attrition Rate %] >= 0.30, "#D62728", -- Red (Critical Alert)
    [Attrition Rate %] >= 0.20, "#FF7F0E", -- Amber (Elevated Risk)
    "#2CA02C"                             -- Green (Healthy Benchmark)
)
```

### 4.3 Dynamic Slicer Context Title
Provides interactive visual headers reflecting applied department filters.
```dax
Dynamic Page Title = 
VAR SelectedDept = SELECTEDVALUE('dim_department'[Department], "All Departments")
RETURN 
"Workforce Intelligence & Attrition Diagnostic - " & SelectedDept
```
