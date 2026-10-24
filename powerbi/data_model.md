# Power BI Data Model Architecture: HR Analytics Star Schema

## 1. Architectural Overview

The Power BI data model is engineered following Kimball dimensional modeling best practices. It implements a clean **Star Schema** with one centralized Fact table (`fact_hr_analytics`) connected to four Dimension tables via single-directional, 1-to-many (`1:*`) relationships.

This star schema structure eliminates circular dependencies, optimizes DAX calculation performance via VertiPaq engine columnar compression, and provides intuitive drill-down paths for business users.

```
                  +-------------------------+
                  |     dim_department      |
                  +-------------------------+
                  | DepartmentID (PK)       |
                  | Department              |
                  +------------+------------+
                               | 1
                               | 
                               | *
+-----------------------+      |      +------------------------+
|    dim_age_group      |      |      |      dim_job_role      |
+-----------------------+      |      +------------------------+
| AgeGroup (PK)         |      |      | JobRoleID (PK)         |
+-----------+-----------+      |      | Department             |
            | 1                |      | JobRole                |
            |                  |      +-----------+------------+
            | *                |                  | 1
+-----------v------------------v------------------v------------+
|                       fact_hr_analytics                      |
+--------------------------------------------------------------+
| EmployeeID (PK)                                              |
| Department (FK)                                              |
| JobRole (FK)                                                 |
| AgeGroup (FK)                                                |
| JobSatisfaction (FK)                                         |
| Salary, AnnualSalary, Age, YearsOfExperience, YearsAtCompany |
| AttendanceRate, AbsenceDays, Overtime, PerformanceRating     |
| WorkLifeBalance, TrainingHours, Attrition, AttritionNumeric  |
| IsActive, SalaryBand, ExperienceBand, TenureBand             |
+------------------------------^-------------------------------+
                               | *
                               | 
                               | 1
                  +------------+------------+
                  |    dim_satisfaction     |
                  +-------------------------+
                  | JobSatisfaction (PK)    |
                  | JobSatisfactionLabel    |
                  | SatisfactionCategory    |
                  +-------------------------+
```

---

## 2. Table Specifications & File Manifest

All Power BI-ready CSV files are located in the `data/processed/` directory:

| Table Name | File Name | Role | Primary Key | Total Records |
| :--- | :--- | :--- | :--- | :--- |
| **Fact HR Analytics** | `fact_hr_analytics.csv` | Central Fact Table | `EmployeeID` | 326 |
| **Dim Department** | `dim_department.csv` | Dimension | `Department` | 3 |
| **Dim Job Role** | `dim_job_role.csv` | Dimension | `JobRole` | 9 |
| **Dim Age Group** | `dim_age_group.csv` | Dimension | `AgeGroup` | 5 |
| **Dim Satisfaction** | `dim_satisfaction.csv` | Dimension | `JobSatisfaction` | 4 |

---

## 3. Relationships & Cardinality

| From (Dimension Table) | Primary Key (PK) | To (Fact Table) | Foreign Key (FK) | Cardinality | Cross Filter Direction |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `dim_department` | `Department` | `fact_hr_analytics` | `Department` | One-to-Many (`1:*`) | Single |
| `dim_job_role` | `JobRole` | `fact_hr_analytics` | `JobRole` | One-to-Many (`1:*`) | Single |
| `dim_age_group` | `AgeGroup` | `fact_hr_analytics` | `AgeGroup` | One-to-Many (`1:*`) | Single |
| `dim_satisfaction` | `JobSatisfaction` | `fact_hr_analytics` | `JobSatisfaction` | One-to-Many (`1:*`) | Single |

> [!NOTE]
> Single-directional cross-filtering (`1:*`) is strictly enforced to prevent ambiguous filter propagation and maximize measure evaluation efficiency.

---

## 4. Sorting & Hierarchy Configurations

To ensure chronological and logical sorting rather than alphabetical ordering in charts and slicers:

1. **`fact_hr_analytics[AgeGroup]`**: Sort by custom index column (`<25` -> 1, `25-34` -> 2, `35-44` -> 3, `45-54` -> 4, `55+` -> 5).
2. **`fact_hr_analytics[SalaryBand]`**: Sort by lower bound of band.
3. **`fact_hr_analytics[TenureBand]`**: Sort by tenure duration (`< 1 Year`, `1-2 Years`, `3-5 Years`, `6-10 Years`, `10+ Years`).
4. **`dim_satisfaction[JobSatisfactionLabel]`**: Sort by `JobSatisfaction` (1, 2, 3, 4).
5. **Organizational Hierarchy**: `Department` > `JobRole` (enables one-click drill-down in Power BI visuals).
