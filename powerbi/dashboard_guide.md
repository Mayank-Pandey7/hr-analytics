# Power BI Dashboard Specification & Implementation Guide

## Executive Dashboard Overview

This guide provides a blueprint for building an enterprise-grade, 4-page interactive HR Analytics Report in **Power BI Desktop**.

- **Canvas Size:** 16:9 widescreen (1280 x 720 px)
- **Design Theme:** Executive Slate & Modern HR Navy
  - Primary Dark / Navigation: `#1E293B` (Slate Navy)
  - Accent / Primary Brand: `#2563EB` (Corporate Cobalt)
  - Alert / High Risk: `#DC2626` (Crimson Alert)
  - Neutral / Card Fill: `#FFFFFF` (Pure White)
  - Canvas Background: `#F8FAFC` (Off-White Cloud)
- **Typography:** Segoe UI / Segoe UI Semibold

---

## Page 1: HR Overview (Executive Cockpit)

### 1.1 Objective
Provide C-Suite and HR executives with an immediate macro-view of workforce size, attrition rate, compensation, tenure, and departmental distribution.

### 1.2 Layout & Component Specifications

#### Top Banner (Y: 0 to 80 px)
- **Title Text:** `Human Resources Analytics & Workforce Overview`
- **Subtitle:** `Executive KPI Monitoring & Organizational Health Diagnostic`
- **Global Slicers Bar (Right):**
  1. `Department` (Dropdown / Tile)
  2. `Gender` (Dropdown)
  3. `Overtime` (Tile: Yes / No)

#### KPI Scorecards Row (Y: 90 to 180 px)
| Visual # | Visual Type | Measure / Field | Display Format | Callout Value Formatting |
| :--- | :--- | :--- | :--- | :--- |
| **KPI 1** | Card (New) | `[Total Employees]` | `#,##0` | 326 |
| **KPI 2** | Card (New) | `[Active Employees]` | `#,##0` | 235 |
| **KPI 3** | Card (New) | `[Attrition Rate %]` | `0.0%` | 27.9% (Conditional Red `#DC2626`) |
| **KPI 4** | Card (New) | `[Avg Monthly Salary]` | `$#,##0` | $3,692 |
| **KPI 5** | Card (New) | `[Avg Company Tenure]` | `0.0 Yrs` | 4.1 Years |
| **KPI 6** | Card (New) | `[Avg Attendance Rate %]` | `0.0%` | 96.1% |

#### Visual 1.1: Headcount & Attrition by Department (Left Panel, Y: 200 to 440 px)
- **Visual Type:** Line and Clustered Column Chart
- **X-Axis:** `fact_hr_analytics[Department]`
- **Column Y-Axis:** `[Total Employees]` (Color: `#2563EB`)
- **Line Y-Axis:** `[Attrition Rate %]` (Color: `#DC2626`, Stroke: 3px, Markers: On)
- **Title:** `Headcount vs Attrition Rate by Department`
- **Tooltip:** `[Active Employees]`, `[Employees Who Left]`, `[Avg Monthly Salary]`

#### Visual 1.2: Workforce Distribution by Job Role (Right Panel, Y: 200 to 440 px)
- **Visual Type:** Clustered Bar Chart (Horizontal)
- **Y-Axis:** `fact_hr_analytics[JobRole]`
- **X-Axis:** `[Total Employees]`
- **Legend / Small Multiple:** `fact_hr_analytics[Department]`
- **Title:** `Employee Count by Job Role and Department`
- **Data Labels:** On

#### Visual 1.3: Age Group & Experience Demographics (Bottom-Left, Y: 460 to 700 px)
- **Visual Type:** Stacked Column Chart
- **X-Axis:** `fact_hr_analytics[AgeGroup]`
- **Y-Axis:** `[Total Employees]`
- **Legend:** `fact_hr_analytics[Attrition]` (`No` = `#3B82F6`, `Yes` = `#EF4444`)
- **Title:** `Age Distribution by Retention Status`

#### Visual 1.4: Tenure & Promotion Velocity Breakdown (Bottom-Right, Y: 460 to 700 px)
- **Visual Type:** Matrix Visual
- **Rows:** `fact_hr_analytics[Department]`, `fact_hr_analytics[JobRole]`
- **Values:** `[Total Employees]`, `[Avg Company Tenure]`, `[Promotion Rate Last 3 Yrs %]`, `[Avg Attendance Rate %]`
- **Title:** `Workforce Tenure & Promotion Metrics by Department & Role`

---

## Page 2: Attrition Analysis (Deep-Dive Root Cause Diagnostic)

### 2.1 Objective
Diagnose the critical drivers of employee departures across workload (overtime), compensation tiers, job satisfaction, and career progression.

### 2.2 Visual Layout & Specifications

#### Visual 2.1: Overtime Attrition Multiplier (Top-Left)
- **Visual Type:** 100% Stacked Bar Chart
- **Y-Axis:** `fact_hr_analytics[Overtime]`
- **X-Axis:** `[Total Employees]`
- **Legend:** `fact_hr_analytics[Attrition]` (`No` = `#94A3B8`, `Yes` = `#DC2626`)
- **Title:** `Attrition Share: Overtime vs Non-Overtime Workers`
- **Insight Callout:** Highlights the 40%+ attrition rate for overtime workers vs ~16% for standard hour staff.

#### Visual 2.2: Attrition by Monthly Salary Band (Top-Right)
- **Visual Type:** Clustered Column Chart
- **X-Axis:** `fact_hr_analytics[SalaryBand]`
- **Y-Axis:** `[Attrition Rate %]`
- **Title:** `Attrition Rate by Salary Band (<$3,500 vs Higher Tiers)`
- **Data Labels:** On (`0.0%`)

#### Visual 2.3: Satisfaction & Work-Life Balance Risk Matrix (Bottom-Left)
- **Visual Type:** Matrix / Heatmap Table
- **Rows:** `fact_hr_analytics[JobSatisfactionLabel]`
- **Columns:** `fact_hr_analytics[WorkLifeBalanceLabel]`
- **Values:** `[Attrition Rate %]`
- **Conditional Formatting:** Background color scaled from Green (Low Attrition) to Dark Red (High Attrition).
- **Title:** `Attrition Risk Matrix: Job Satisfaction vs Work-Life Balance (%)`

#### Visual 2.4: Attrition by Company Tenure & Career Stagnation (Bottom-Right)
- **Visual Type:** Clustered Bar Chart
- **Y-Axis:** `fact_hr_analytics[TenureBand]`
- **X-Axis:** `[Attrition Rate %]`
- **Legend:** `fact_hr_analytics[PromotionInLast3Years]`
- **Title:** `Attrition by Company Tenure & Recent Promotion History`

---

## Page 3: Performance & Workforce Dynamics

### 3.1 Objective
Analyze talent quality, appraisal distributions, attendance and absenteeism correlations, and training ROI.

### 3.2 Visual Layout & Specifications

#### Visual 3.1: Compensation vs Experience Equity Curve (Top-Left)
- **Visual Type:** Scatter Chart
- **X-Axis:** `fact_hr_analytics[YearsOfExperience]`
- **Y-Axis:** `fact_hr_analytics[Salary]`
- **Legend:** `fact_hr_analytics[Attrition]`
- **Size:** `fact_hr_analytics[PerformanceRating]`
- **Title:** `Monthly Salary vs Total Experience by Attrition Cohort`

#### Visual 3.2: Department Performance & Attendance Benchmark (Top-Right)
- **Visual Type:** Clustered Bar Chart
- **Y-Axis:** `fact_hr_analytics[Department]`
- **X-Axis:** `[Avg Performance Rating]`
- **Tooltip:** `[Avg Attendance Rate %]`, `[Avg Absence Days]`
- **Title:** `Average Appraisal Rating by Department`

#### Visual 3.3: Absenteeism Distribution by Retention Cohort (Bottom-Left)
- **Visual Type:** Clustered Column Chart
- **X-Axis:** `fact_hr_analytics[AbsenceDays]` (binned: 0-5, 6-10, 11-15, 16-20, 20+)
- **Y-Axis:** `[Total Employees]`
- **Legend:** `fact_hr_analytics[Attrition]`
- **Title:** `Absenteeism Frequency Distribution (Departed vs Retained)`

#### Visual 3.4: Training Investment & Performance Interaction (Bottom-Right)
- **Visual Type:** Clustered Bar Chart
- **X-Axis:** `fact_hr_analytics[PerformanceRatingLabel]`
- **Y-Axis:** `Average of TrainingHours`
- **Title:** `Average Training Hours Invested by Performance Rating Tier`

---

## Page 4: Strategic HR Recommendations & Risk Mitigation

### 4.1 Objective
Present executive leadership with evidence-based business insights, identified high-attrition segments, concrete retention policies, and data limitations.

### 4.2 Layout & Content Cards

#### Card 4.1: Critical Risk Cohort Identification (Top Banner)
- **Highlighted Metric:** `Critical Risk Segment Headcount: 32 Employees | Attrition Rate: 62.5%`
- **Definition:** Employees subject to simultaneous Overtime = Yes, Satisfaction <= 2, and Salary < $5,000.

#### Card 4.2: Four Pillars of Actionable Intervention
1. **Pillar 1: Overtime Normalization & Workload Caps**
   - Mandate maximum weekly overtime caps (no more than 8 overtime hours/week).
   - Establish compensatory off (comp-off) days for overtime workers to prevent burnout.
2. **Pillar 2: Entry-Level Salary Benchmarking**
   - Conduct compensation equity audit for Laboratory Technicians and Sales Representatives earning under $3,500.
   - Adjust baseline pay to regional median to remove compensation as a flight trigger.
3. **Pillar 3: Early-Tenure Onboarding & Career Pathing**
   - Implement structured 30-60-90 day milestone reviews for staff in their first 2 years.
   - Provide clear promotion visibility and technical skill development tracks.
4. **Pillar 4: Departmental Burnout Interventions in Sales & HR**
   - Review commission quota realism in Sales; streamline administrative load in HR.

#### Card 4.3: Analytical Limitations & Assumptions
- Cross-sectional observational dataset; statistical correlation does not establish direct causation.
- Exit interview qualitative commentary (manager friction, external market offers) is unobserved.
- Recommend continuous quarterly pulse surveys to validate sentiment trends over time.

---

## 5. Step-by-Step Power BI Desktop Import Tutorial

1. Open **Power BI Desktop**.
2. Click **Get Data** > **Text/CSV**.
3. Navigate to `data/processed/` and select `fact_hr_analytics.csv`. Click **Load**.
4. Repeat for `dim_department.csv`, `dim_job_role.csv`, `dim_age_group.csv`, and `dim_satisfaction.csv`.
5. Navigate to the **Model View** (left rail icon):
   - Confirm all 4 single-directional 1-to-many relationships as documented in `powerbi/data_model.md`.
6. Click **Modeling** > **New Table** to create the `_Measures` table:
   ```dax
   _Measures = ROW("Description", "HR DAX Measures")
   ```
7. Click **New Measure** and paste each DAX measure from `powerbi/dax_measures.md`.
8. Switch to **Report View** and construct the 4 pages using the specifications above.
9. Save project as `HR_Analytics_Dashboard.pbix`.
