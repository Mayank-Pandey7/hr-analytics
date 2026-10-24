"""
Builds a standalone interactive web dashboard (outputs/dashboard.html & index.html)
Allows anyone to open the project in any browser without installing Python or Power BI.
Includes live interactive filters, dynamic KPI cards, Chart.js visuals, and tab navigation.
"""

import json
import os
import pandas as pd

def build_dashboard():
    df = pd.read_csv('data/processed/fact_hr_analytics.csv')
    
    # Export clean minimal records for client-side JS filtering
    records = df[[
        'EmployeeID', 'Department', 'JobRole', 'Gender', 'Age', 'AgeGroup',
        'Salary', 'AnnualSalary', 'SalaryBand', 'YearsOfExperience', 'YearsAtCompany',
        'AttendanceRate', 'AbsenceDays', 'Overtime', 'JobSatisfaction',
        'PerformanceRating', 'WorkLifeBalance', 'Attrition', 'AttritionNumeric', 'IsActive'
    ]].to_dict(orient='records')

    records_json = json.dumps(records)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HR Analytics & Workforce Intelligence Dashboard</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; background-color: #0f172a; color: #f8fafc; }}
        .card {{ background-color: #1e293b; border: 1px solid #334155; }}
        .tab-active {{ border-bottom: 3px solid #38bdf8; color: #38bdf8; font-weight: 600; }}
        .tab-inactive {{ color: #94a3b8; border-bottom: 3px solid transparent; }}
        .tab-inactive:hover {{ color: #cbd5e1; }}
    </style>
</head>
<body class="min-h-screen flex flex-col">

    <!-- Top Navigation Header -->
    <header class="bg-slate-900 border-b border-slate-800 px-6 py-4 flex flex-wrap items-center justify-between gap-4 sticky top-0 z-50 shadow-lg">
        <div class="flex items-center space-x-3">
            <div class="w-10 h-10 rounded-lg bg-sky-500/10 border border-sky-500/30 flex items-center justify-center text-sky-400 font-bold text-xl">
                HR
            </div>
            <div>
                <h1 class="text-xl font-bold tracking-tight text-white flex items-center gap-2">
                    Workforce Intelligence & Attrition Diagnostic
                    <span class="text-xs font-semibold uppercase px-2 py-0.5 rounded bg-sky-500/20 text-sky-400 border border-sky-500/30">Enterprise Edition</span>
                </h1>
                <p class="text-xs text-slate-400">Executive People Analytics Dashboard | Python & SQL Analytical Pipeline</p>
            </div>
        </div>

        <!-- Global Interactive Slicers -->
        <div class="flex flex-wrap items-center gap-3">
            <div>
                <label class="text-[11px] font-medium text-slate-400 block mb-1">Department</label>
                <select id="filterDept" onchange="applyFilters()" class="bg-slate-800 border border-slate-700 text-xs rounded-md px-3 py-1.5 text-slate-200 focus:outline-none focus:border-sky-500">
                    <option value="ALL">All Departments</option>
                    <option value="Research & Development">Research & Development</option>
                    <option value="Sales">Sales</option>
                    <option value="Human Resources">Human Resources</option>
                </select>
            </div>
            <div>
                <label class="text-[11px] font-medium text-slate-400 block mb-1">Overtime</label>
                <select id="filterOvertime" onchange="applyFilters()" class="bg-slate-800 border border-slate-700 text-xs rounded-md px-3 py-1.5 text-slate-200 focus:outline-none focus:border-sky-500">
                    <option value="ALL">All Workers</option>
                    <option value="Yes">Overtime (Yes)</option>
                    <option value="No">No Overtime</option>
                </select>
            </div>
            <div>
                <label class="text-[11px] font-medium text-slate-400 block mb-1">Gender</label>
                <select id="filterGender" onchange="applyFilters()" class="bg-slate-800 border border-slate-700 text-xs rounded-md px-3 py-1.5 text-slate-200 focus:outline-none focus:border-sky-500">
                    <option value="ALL">All Genders</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                </select>
            </div>
            <div class="pt-4">
                <button onclick="resetFilters()" class="bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium px-3 py-1.5 rounded border border-slate-700 transition">
                    Reset Filters
                </button>
            </div>
        </div>
    </header>

    <!-- Navigation Tabs -->
    <div class="bg-slate-900/60 border-b border-slate-800 px-6">
        <nav class="flex space-x-8 text-sm">
            <button onclick="switchTab('page1')" id="tab-page1" class="py-3 px-1 tab-active transition flex items-center gap-2">
                <span>📊</span> 1. HR Overview
            </button>
            <button onclick="switchTab('page2')" id="tab-page2" class="py-3 px-1 tab-inactive transition flex items-center gap-2">
                <span>🚨</span> 2. Attrition Diagnostic
            </button>
            <button onclick="switchTab('page3')" id="tab-page3" class="py-3 px-1 tab-inactive transition flex items-center gap-2">
                <span>🎯</span> 3. Performance & Workforce
            </button>
            <button onclick="switchTab('page4')" id="tab-page4" class="py-3 px-1 tab-inactive transition flex items-center gap-2">
                <span>💡</span> 4. Strategic Actions
            </button>
        </nav>
    </div>

    <!-- Main Dashboard Container -->
    <main class="flex-1 p-6 max-w-7xl mx-auto w-full space-y-6">

        <!-- Dynamic Executive KPI Scorecards -->
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
            <div class="card p-4 rounded-xl shadow-sm">
                <p class="text-xs font-medium text-slate-400">Total Workforce</p>
                <h3 id="kpiTotal" class="text-2xl font-bold text-white mt-1">326</h3>
                <span class="text-[11px] text-slate-500">Filtered population</span>
            </div>
            <div class="card p-4 rounded-xl shadow-sm">
                <p class="text-xs font-medium text-slate-400">Active Employees</p>
                <h3 id="kpiActive" class="text-2xl font-bold text-emerald-400 mt-1">235</h3>
                <span id="kpiActivePct" class="text-[11px] text-emerald-500 font-medium">72.1% Retained</span>
            </div>
            <div class="card p-4 rounded-xl shadow-sm border-l-4 border-l-red-500">
                <p class="text-xs font-medium text-slate-400">Overall Attrition</p>
                <h3 id="kpiAttritionRate" class="text-2xl font-bold text-rose-400 mt-1">27.9%</h3>
                <span id="kpiLeftCount" class="text-[11px] text-rose-500 font-medium">91 departures</span>
            </div>
            <div class="card p-4 rounded-xl shadow-sm">
                <p class="text-xs font-medium text-slate-400">Avg Monthly Salary</p>
                <h3 id="kpiSalary" class="text-2xl font-bold text-white mt-1">$3,692</h3>
                <span class="text-[11px] text-slate-400">Annual: $44.3k</span>
            </div>
            <div class="card p-4 rounded-xl shadow-sm">
                <p class="text-xs font-medium text-slate-400">Overtime Rate</p>
                <h3 id="kpiOvertime" class="text-2xl font-bold text-amber-400 mt-1">28.8%</h3>
                <span class="text-[11px] text-slate-500">94 staff on OT</span>
            </div>
            <div class="card p-4 rounded-xl shadow-sm">
                <p class="text-xs font-medium text-slate-400">Avg Tenure</p>
                <h3 id="kpiTenure" class="text-2xl font-bold text-sky-400 mt-1">4.1 yrs</h3>
                <span class="text-[11px] text-slate-500">Experience: 5.0 yrs</span>
            </div>
        </div>

        <!-- ================= PAGE 1: HR OVERVIEW ================= -->
        <div id="view-page1" class="space-y-6">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Department Headcount & Attrition Chart -->
                <div class="card p-5 rounded-xl shadow-md">
                    <div class="flex items-center justify-between mb-4">
                        <h2 class="text-sm font-semibold text-white">Department Headcount & Attrition Rate (%)</h2>
                        <span class="text-xs text-slate-400">Bars: Count | Line: %</span>
                    </div>
                    <div class="h-64">
                        <canvas id="chartDept"></canvas>
                    </div>
                </div>

                <!-- Job Role Breakdown -->
                <div class="card p-5 rounded-xl shadow-md">
                    <div class="flex items-center justify-between mb-4">
                        <h2 class="text-sm font-semibold text-white">Attrition Rate by Job Role (%)</h2>
                        <span class="text-xs text-rose-400 font-medium">Critical Threshold: &gt;30%</span>
                    </div>
                    <div class="h-64">
                        <canvas id="chartRole"></canvas>
                    </div>
                </div>
            </div>

            <!-- Demographics and Tenure Grid -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div class="card p-5 rounded-xl shadow-md">
                    <h2 class="text-sm font-semibold text-white mb-3">Headcount by Age Group</h2>
                    <div class="h-56">
                        <canvas id="chartAge"></canvas>
                    </div>
                </div>
                <div class="card p-5 rounded-xl shadow-md">
                    <h2 class="text-sm font-semibold text-white mb-3">Company Tenure Distribution</h2>
                    <div class="h-56">
                        <canvas id="chartTenure"></canvas>
                    </div>
                </div>
                <div class="card p-5 rounded-xl shadow-md flex flex-col justify-between">
                    <div>
                        <h2 class="text-sm font-semibold text-white mb-3">Executive Summary Insights</h2>
                        <div class="space-y-3 text-xs text-slate-300">
                            <div class="p-2.5 rounded-lg bg-slate-800/80 border border-slate-700">
                                <span class="font-semibold text-rose-400">Department Drain:</span> Human Resources experiences the highest relative attrition (**46.2%**), followed by Sales (**31.3%**).
                            </div>
                            <div class="p-2.5 rounded-lg bg-slate-800/80 border border-slate-700">
                                <span class="font-semibold text-amber-400">High Risk Roles:</span> Sales Representatives (57.1%) and Laboratory Technicians (38.8%) represent high-turnover entry hubs.
                            </div>
                            <div class="p-2.5 rounded-lg bg-slate-800/80 border border-slate-700">
                                <span class="font-semibold text-sky-400">Tenure Window:</span> 46.2% of first-year staff leave, stabilizing once employees cross 3 years of tenure.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ================= PAGE 2: ATTRITION DIAGNOSTIC ================= -->
        <div id="view-page2" class="space-y-6 hidden">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Overtime Attrition Multiplier -->
                <div class="card p-5 rounded-xl shadow-md">
                    <div class="flex items-center justify-between mb-4">
                        <div>
                            <h2 class="text-sm font-semibold text-white">Overtime Impact on Attrition Rate</h2>
                            <p class="text-xs text-slate-400">Statistical Significance: p = 2.30e-10 (Extreme)</p>
                        </div>
                        <span class="text-xs px-2 py-1 rounded bg-rose-500/20 text-rose-400 font-bold border border-rose-500/30">3.4x Risk Factor</span>
                    </div>
                    <div class="h-64">
                        <canvas id="chartOvertime"></canvas>
                    </div>
                </div>

                <!-- Salary Band Breakdown -->
                <div class="card p-5 rounded-xl shadow-md">
                    <div class="flex items-center justify-between mb-4">
                        <div>
                            <h2 class="text-sm font-semibold text-white">Attrition Rate by Monthly Salary Band</h2>
                            <p class="text-xs text-slate-400">Mann-Whitney U Test: p = 6.58e-06</p>
                        </div>
                        <span class="text-xs text-slate-400">Median Leavers: $2,515</span>
                    </div>
                    <div class="h-64">
                        <canvas id="chartSalaryBand"></canvas>
                    </div>
                </div>
            </div>

            <!-- Satisfaction vs Balance Matrix -->
            <div class="card p-5 rounded-xl shadow-md">
                <h2 class="text-sm font-semibold text-white mb-2">Multi-Factor Critical Risk Segment Analysis</h2>
                <p class="text-xs text-slate-400 mb-4">Empirical breakdown comparing the high-risk compounder segment against organization baseline</p>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
                    <div class="p-4 rounded-lg bg-rose-950/40 border border-rose-900/50">
                        <span class="font-bold text-rose-400 text-sm block mb-1">🚨 Critical Risk Segment</span>
                        <p class="text-slate-300 mb-2">Criteria: Overtime = Yes + JobSat &le; 2 + Salary &lt; $5,000</p>
                        <div class="flex justify-between border-t border-rose-900/40 pt-2 text-slate-200">
                            <span>Headcount: <strong>32 staff</strong></span>
                            <span class="text-rose-400 font-bold text-sm">62.5% Attrition</span>
                        </div>
                    </div>
                    <div class="p-4 rounded-lg bg-amber-950/40 border border-amber-900/50">
                        <span class="font-bold text-amber-400 text-sm block mb-1">⚠️ Moderate Risk Segment</span>
                        <p class="text-slate-300 mb-2">Criteria: Any 1 or 2 of the risk criteria present</p>
                        <div class="flex justify-between border-t border-amber-900/40 pt-2 text-slate-200">
                            <span>Headcount: <strong>272 staff</strong></span>
                            <span class="text-amber-400 font-bold text-sm">25.7% Attrition</span>
                        </div>
                    </div>
                    <div class="p-4 rounded-lg bg-emerald-950/40 border border-emerald-900/50">
                        <span class="font-bold text-emerald-400 text-sm block mb-1">✅ Low Risk (Protected)</span>
                        <p class="text-slate-300 mb-2">Criteria: No Overtime + JobSat &ge; 3 + Salary &ge; $5,000</p>
                        <div class="flex justify-between border-t border-emerald-900/40 pt-2 text-slate-200">
                            <span>Headcount: <strong>22 staff</strong></span>
                            <span class="text-emerald-400 font-bold text-sm">4.5% Attrition</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ================= PAGE 3: PERFORMANCE & WORKFORCE ================= -->
        <div id="view-page3" class="space-y-6 hidden">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Salary vs Experience Scatter -->
                <div class="card p-5 rounded-xl shadow-md">
                    <h2 class="text-sm font-semibold text-white mb-2">Salary vs Years of Experience by Retention Cohort</h2>
                    <p class="text-xs text-slate-400 mb-4">Blue = Retained | Red = Departed</p>
                    <div class="h-64">
                        <canvas id="chartScatter"></canvas>
                    </div>
                </div>

                <!-- Department Appraisal Scores -->
                <div class="card p-5 rounded-xl shadow-md">
                    <h2 class="text-sm font-semibold text-white mb-2">Average Performance Rating by Department</h2>
                    <p class="text-xs text-slate-400 mb-4">Benchmark Rating Scale: 1 (Low) to 4 (Outstanding)</p>
                    <div class="h-64">
                        <canvas id="chartPerf"></canvas>
                    </div>
                </div>
            </div>

            <!-- Attendance & Absenteeism Metrics -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="card p-5 rounded-xl shadow-md">
                    <h2 class="text-sm font-semibold text-white mb-2">Attendance & Absenteeism Health</h2>
                    <p class="text-xs text-slate-400 mb-4">Annualized corporate absence days across cohorts</p>
                    <div class="space-y-3 text-xs">
                        <div class="flex justify-between p-3 rounded bg-slate-800 border border-slate-700">
                            <span class="text-slate-400">Organization Average Attendance:</span>
                            <span class="font-bold text-emerald-400">96.12%</span>
                        </div>
                        <div class="flex justify-between p-3 rounded bg-slate-800 border border-slate-700">
                            <span class="text-slate-400">Avg Absent Days (Retained Staff):</span>
                            <span class="font-bold text-slate-200">9.60 Days</span>
                        </div>
                        <div class="flex justify-between p-3 rounded bg-slate-800 border border-slate-700">
                            <span class="text-slate-400">Avg Absent Days (Departed Staff):</span>
                            <span class="font-bold text-rose-400">9.91 Days</span>
                        </div>
                    </div>
                </div>

                <div class="card p-5 rounded-xl shadow-md">
                    <h2 class="text-sm font-semibold text-white mb-2">Interpretable ML Model Summary</h2>
                    <p class="text-xs text-slate-400 mb-3">Balanced Logistic Regression (Test AUC: 0.692 | Recall: 61%)</p>
                    <div class="text-xs space-y-2 text-slate-300">
                        <p><span class="font-semibold text-rose-400">1. Overtime:</span> Multiplies departure odds by +3.45x ($p < 0.0001$).</p>
                        <p><span class="font-semibold text-emerald-400">2. Salary:</span> Acts as the primary retention buffer (-0.62 coef per std dev).</p>
                        <p><span class="font-semibold text-amber-400">3. Marital Status:</span> Singles experience 1.6x higher departure velocity.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- ================= PAGE 4: STRATEGIC RECOMMENDATIONS ================= -->
        <div id="view-page4" class="space-y-6 hidden">
            <div class="card p-6 rounded-xl border-l-4 border-l-sky-500 shadow-md">
                <h2 class="text-base font-bold text-white mb-2">Executive Retention Strategy & Management Action Plan</h2>
                <p class="text-xs text-slate-300 leading-relaxed">
                    Based on rigorous empirical validation across 326 employees, attrition is not caused by poor performance or lack of promotions. Rather, it is concentrated in an unsustainable operational interaction between overtime workload and sub-market entry compensation.
                </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Pillar 1 -->
                <div class="card p-5 rounded-xl">
                    <div class="flex items-center gap-2 mb-2">
                        <span class="w-6 h-6 rounded-full bg-rose-500/20 text-rose-400 flex items-center justify-center font-bold text-xs">1</span>
                        <h3 class="text-sm font-bold text-white">Workload Governance & Overtime Normalization</h3>
                    </div>
                    <p class="text-xs text-slate-300 leading-relaxed mb-3">
                        Overtime drives attrition from 16.4% to 56.4% (3.4x multiplier). 
                    </p>
                    <ul class="text-xs text-slate-400 space-y-1.5 list-disc list-inside">
                        <li>Implement a hard cap of 8 overtime hours per week per employee.</li>
                        <li>Provide 1:1 compensatory off (comp-off) days for overtime within 30 days.</li>
                        <li>Add shift coverage for Laboratory Technicians and Sales Reps.</li>
                    </ul>
                </div>

                <!-- Pillar 2 -->
                <div class="card p-5 rounded-xl">
                    <div class="flex items-center gap-2 mb-2">
                        <span class="w-6 h-6 rounded-full bg-amber-500/20 text-amber-400 flex items-center justify-center font-bold text-xs">2</span>
                        <h3 class="text-sm font-bold text-white">Entry-Level Compensation Realignment</h3>
                    </div>
                    <p class="text-xs text-slate-300 leading-relaxed mb-3">
                        Attrition in the &lt;$3,500 band is 41.7% (median leaver salary: $2,515 vs $3,375).
                    </p>
                    <ul class="text-xs text-slate-400 space-y-1.5 list-disc list-inside">
                        <li>Raise base entry salaries for Sales Reps and Lab Techs to $3,200-$3,500 threshold.</li>
                        <li>Restructure Sales compensation to increase fixed base pay by 15%.</li>
                        <li>Conduct annual compensation parity audits against regional benchmarks.</li>
                    </ul>
                </div>

                <!-- Pillar 3 -->
                <div class="card p-5 rounded-xl">
                    <div class="flex items-center gap-2 mb-2">
                        <span class="w-6 h-6 rounded-full bg-sky-500/20 text-sky-400 flex items-center justify-center font-bold text-xs">3</span>
                        <h3 class="text-sm font-bold text-white">First-Year Onboarding & Mentorship</h3>
                    </div>
                    <p class="text-xs text-slate-300 leading-relaxed mb-3">
                        46.2% of staff in their first year at the company depart.
                    </p>
                    <ul class="text-xs text-slate-400 space-y-1.5 list-disc list-inside">
                        <li>Pair young new hires (&lt;25) with tenured mentors (&gt;5 yrs tenure).</li>
                        <li>Schedule formal 30-60-90 day check-ins led by HR Business Partners.</li>
                        <li>Clarify promotional milestones and technical career tracks early.</li>
                    </ul>
                </div>

                <!-- Pillar 4 -->
                <div class="card p-5 rounded-xl">
                    <div class="flex items-center gap-2 mb-2">
                        <span class="w-6 h-6 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold text-xs">4</span>
                        <h3 class="text-sm font-bold text-white">HR Division Administrative Restructuring</h3>
                    </div>
                    <p class="text-xs text-slate-300 leading-relaxed mb-3">
                        Human Resources suffered the highest attrition rate of any division (46.2%).
                    </p>
                    <ul class="text-xs text-slate-400 space-y-1.5 list-disc list-inside">
                        <li>Deploy HR ticketing software to reduce repetitive manual documentation.</li>
                        <li>Adjust HR Specialist compensation to market parity ($3,500+).</li>
                        <li>Implement quarterly anonymous workload pulse surveys.</li>
                    </ul>
                </div>
            </div>
        </div>

    </main>

    <!-- Footer -->
    <footer class="bg-slate-900 border-t border-slate-800 px-6 py-4 text-center text-xs text-slate-500 mt-auto">
        HR Analytics & Employee Attrition Portfolio Project | Built with Python, SQL & Power BI | Open Source & Reproducible
    </footer>

    <!-- Client-side Analytics & Visualization Script -->
    <script>
        const RAW_DATA = {records_json};

        let currentTab = 'page1';
        let chartInstances = {{}};

        function switchTab(tabId) {{
            ['page1', 'page2', 'page3', 'page4'].forEach(t => {{
                document.getElementById('view-' + t).classList.add('hidden');
                document.getElementById('tab-' + t).className = 'py-3 px-1 tab-inactive transition flex items-center gap-2';
            }});
            document.getElementById('view-' + tabId).classList.remove('hidden');
            document.getElementById('tab-' + tabId).className = 'py-3 px-1 tab-active transition flex items-center gap-2';
            currentTab = tabId;
            renderCharts();
        }}

        function getFilteredData() {{
            const dept = document.getElementById('filterDept').value;
            const ot = document.getElementById('filterOvertime').value;
            const gender = document.getElementById('filterGender').value;

            return RAW_DATA.filter(row => {{
                if (dept !== 'ALL' && row.Department !== dept) return false;
                if (ot !== 'ALL' && row.Overtime !== ot) return false;
                if (gender !== 'ALL' && row.Gender !== gender) return false;
                return true;
            }});
        }}

        function updateKPIs(data) {{
            const total = data.length;
            if (total === 0) {{
                document.getElementById('kpiTotal').innerText = '0';
                document.getElementById('kpiActive').innerText = '0';
                document.getElementById('kpiAttritionRate').innerText = '0.0%';
                return;
            }}
            const active = data.filter(d => d.Attrition === 'No').length;
            const departed = data.filter(d => d.Attrition === 'Yes').length;
            const rate = ((departed / total) * 100).toFixed(1);
            const activePct = ((active / total) * 100).toFixed(1);
            const avgSal = Math.round(data.reduce((a, b) => a + b.Salary, 0) / total);
            const otCount = data.filter(d => d.Overtime === 'Yes').length;
            const otPct = ((otCount / total) * 100).toFixed(1);
            const avgTenure = (data.reduce((a, b) => a + b.YearsAtCompany, 0) / total).toFixed(1);

            document.getElementById('kpiTotal').innerText = total.toLocaleString();
            document.getElementById('kpiActive').innerText = active.toLocaleString();
            document.getElementById('kpiActivePct').innerText = activePct + '% Retained';
            document.getElementById('kpiAttritionRate').innerText = rate + '%';
            document.getElementById('kpiLeftCount').innerText = departed + ' departures';
            document.getElementById('kpiSalary').innerText = '$' + avgSal.toLocaleString();
            document.getElementById('kpiOvertime').innerText = otPct + '%';
            document.getElementById('kpiTenure').innerText = avgTenure + ' yrs';
        }}

        function applyFilters() {{
            const data = getFilteredData();
            updateKPIs(data);
            renderCharts();
        }}

        function resetFilters() {{
            document.getElementById('filterDept').value = 'ALL';
            document.getElementById('filterOvertime').value = 'ALL';
            document.getElementById('filterGender').value = 'ALL';
            applyFilters();
        }}

        function destroyChart(id) {{
            if (chartInstances[id]) {{
                chartInstances[id].destroy();
                delete chartInstances[id];
            }}
        }}

        function renderCharts() {{
            const data = getFilteredData();

            if (currentTab === 'page1') {{
                // Dept Headcount & Attrition
                destroyChart('chartDept');
                const depts = [...new Set(data.map(d => d.Department))];
                const deptCounts = depts.map(d => data.filter(x => x.Department === d).length);
                const deptRates = depts.map(d => {{
                    const sub = data.filter(x => x.Department === d);
                    return sub.length ? ((sub.filter(x => x.Attrition === 'Yes').length / sub.length) * 100).toFixed(1) : 0;
                }});

                const ctxDept = document.getElementById('chartDept').getContext('2d');
                chartInstances['chartDept'] = new Chart(ctxDept, {{
                    type: 'bar',
                    data: {{
                        labels: depts,
                        datasets: [
                            {{
                                label: 'Headcount',
                                data: deptCounts,
                                backgroundColor: '#2563eb',
                                yAxisID: 'y'
                            }},
                            {{
                                label: 'Attrition %',
                                data: deptRates,
                                borderColor: '#f43f5e',
                                backgroundColor: '#f43f5e',
                                type: 'line',
                                yAxisID: 'y1',
                                borderWidth: 2,
                                pointRadius: 4
                            }}
                        ]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            x: {{ ticks: {{ color: '#94a3b8' }}, grid: {{ color: '#334155' }} }},
                            y: {{ type: 'linear', position: 'left', ticks: {{ color: '#94a3b8' }}, grid: {{ color: '#334155' }} }},
                            y1: {{ type: 'linear', position: 'right', ticks: {{ color: '#f43f5e', callback: v => v + '%' }}, grid: {{ display: false }} }}
                        }},
                        plugins: {{ legend: {{ labels: {{ color: '#cbd5e1' }} }} }}
                    }}
                }});

                // Role Attrition Rate
                destroyChart('chartRole');
                const roles = [...new Set(data.map(d => d.JobRole))];
                const roleStats = roles.map(r => {{
                    const sub = data.filter(x => x.JobRole === r);
                    const rate = sub.length ? ((sub.filter(x => x.Attrition === 'Yes').length / sub.length) * 100) : 0;
                    return {{ role: r, rate: rate }};
                }}).sort((a, b) => b.rate - a.rate);

                const ctxRole = document.getElementById('chartRole').getContext('2d');
                chartInstances['chartRole'] = new Chart(ctxRole, {{
                    type: 'bar',
                    data: {{
                        labels: roleStats.map(r => r.role),
                        datasets: [{{
                            label: 'Attrition Rate %',
                            data: roleStats.map(r => r.rate.toFixed(1)),
                            backgroundColor: roleStats.map(r => r.rate >= 30 ? '#f43f5e' : '#38bdf8')
                        }}]
                    }},
                    options: {{
                        indexAxis: 'y',
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            x: {{ ticks: {{ color: '#94a3b8', callback: v => v + '%' }}, grid: {{ color: '#334155' }} }},
                            y: {{ ticks: {{ color: '#cbd5e1' }}, grid: {{ display: false }} }}
                        }},
                        plugins: {{ legend: {{ display: false }} }}
                    }}
                }});

                // Age Distribution
                destroyChart('chartAge');
                const ageGroups = ['<25', '25-34', '35-44', '45-54', '55+'];
                const ageCounts = ageGroups.map(g => data.filter(x => x.AgeGroup === g).length);
                const ctxAge = document.getElementById('chartAge').getContext('2d');
                chartInstances['chartAge'] = new Chart(ctxAge, {{
                    type: 'doughnut',
                    data: {{
                        labels: ageGroups,
                        datasets: [{{
                            data: ageCounts,
                            backgroundColor: ['#f43f5e', '#38bdf8', '#3b82f6', '#10b981', '#f59e0b']
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{ legend: {{ position: 'right', labels: {{ color: '#cbd5e1', boxWidth: 12 }} }} }}
                    }}
                }});

                // Tenure Distribution
                destroyChart('chartTenure');
                const tenureBins = ['< 1 Yr', '1-2 Yrs', '3-5 Yrs', '6-10 Yrs', '10+ Yrs'];
                const tenureCounts = [
                    data.filter(x => x.YearsAtCompany < 1).length,
                    data.filter(x => x.YearsAtCompany >= 1 && x.YearsAtCompany <= 2).length,
                    data.filter(x => x.YearsAtCompany >= 3 && x.YearsAtCompany <= 5).length,
                    data.filter(x => x.YearsAtCompany >= 6 && x.YearsAtCompany <= 10).length,
                    data.filter(x => x.YearsAtCompany > 10).length,
                ];
                const ctxTenure = document.getElementById('chartTenure').getContext('2d');
                chartInstances['chartTenure'] = new Chart(ctxTenure, {{
                    type: 'bar',
                    data: {{
                        labels: tenureBins,
                        datasets: [{{
                            label: 'Headcount',
                            data: tenureCounts,
                            backgroundColor: '#6366f1'
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            x: {{ ticks: {{ color: '#94a3b8' }}, grid: {{ display: false }} }},
                            y: {{ ticks: {{ color: '#94a3b8' }}, grid: {{ color: '#334155' }} }}
                        }},
                        plugins: {{ legend: {{ display: false }} }}
                    }}
                }});
            }}

            if (currentTab === 'page2') {{
                // Overtime chart
                destroyChart('chartOvertime');
                const otYes = data.filter(x => x.Overtime === 'Yes');
                const otNo = data.filter(x => x.Overtime === 'No');
                const otYesRate = otYes.length ? ((otYes.filter(x => x.Attrition === 'Yes').length / otYes.length) * 100).toFixed(1) : 0;
                const otNoRate = otNo.length ? ((otNo.filter(x => x.Attrition === 'Yes').length / otNo.length) * 100).toFixed(1) : 0;

                const ctxOt = document.getElementById('chartOvertime').getContext('2d');
                chartInstances['chartOvertime'] = new Chart(ctxOt, {{
                    type: 'bar',
                    data: {{
                        labels: ['No Overtime (Standard)', 'Overtime Worker'],
                        datasets: [{{
                            label: 'Attrition Rate %',
                            data: [otNoRate, otYesRate],
                            backgroundColor: ['#3b82f6', '#f43f5e']
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            x: {{ ticks: {{ color: '#cbd5e1' }}, grid: {{ display: false }} }},
                            y: {{ ticks: {{ color: '#94a3b8', callback: v => v + '%' }}, max: 100, grid: {{ color: '#334155' }} }}
                        }},
                        plugins: {{ legend: {{ display: false }} }}
                    }}
                }});

                // Salary Band chart
                destroyChart('chartSalaryBand');
                const salBands = ['< $3,500 (Entry)', '$3,500 - $6,999 (Mid)', '$7,000 - $11,999 (Senior)', '$12,000+ (Executive)'];
                const salRates = salBands.map(b => {{
                    const sub = data.filter(x => x.SalaryBand === b);
                    return sub.length ? ((sub.filter(x => x.Attrition === 'Yes').length / sub.length) * 100).toFixed(1) : 0;
                }});

                const ctxSal = document.getElementById('chartSalaryBand').getContext('2d');
                chartInstances['chartSalaryBand'] = new Chart(ctxSal, {{
                    type: 'bar',
                    data: {{
                        labels: ['< $3.5k', '$3.5k-$7k', '$7k-$12k', '$12k+'],
                        datasets: [{{
                            label: 'Attrition %',
                            data: salRates,
                            backgroundColor: ['#f43f5e', '#fb923c', '#38bdf8', '#10b981']
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            x: {{ ticks: {{ color: '#cbd5e1' }}, grid: {{ display: false }} }},
                            y: {{ ticks: {{ color: '#94a3b8', callback: v => v + '%' }}, max: 60, grid: {{ color: '#334155' }} }}
                        }},
                        plugins: {{ legend: {{ display: false }} }}
                    }}
                }});
            }}

            if (currentTab === 'page3') {{
                // Scatter chart: Salary vs Experience
                destroyChart('chartScatter');
                const scatterRetained = data.filter(x => x.Attrition === 'No').map(x => ({{ x: x.YearsOfExperience, y: x.Salary }}));
                const scatterAttrited = data.filter(x => x.Attrition === 'Yes').map(x => ({{ x: x.YearsOfExperience, y: x.Salary }}));

                const ctxScat = document.getElementById('chartScatter').getContext('2d');
                chartInstances['chartScatter'] = new Chart(ctxScat, {{
                    type: 'scatter',
                    data: {{
                        datasets: [
                            {{ label: 'Retained', data: scatterRetained, backgroundColor: '#38bdf8' }},
                            {{ label: 'Attrited', data: scatterAttrited, backgroundColor: '#f43f5e' }}
                        ]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            x: {{ title: {{ display: true, text: 'Total Years of Experience', color: '#94a3b8' }}, ticks: {{ color: '#94a3b8' }}, grid: {{ color: '#334155' }} }},
                            y: {{ title: {{ display: true, text: 'Monthly Salary ($)', color: '#94a3b8' }}, ticks: {{ color: '#94a3b8' }}, grid: {{ color: '#334155' }} }}
                        }},
                        plugins: {{ legend: {{ labels: {{ color: '#cbd5e1' }} }} }}
                    }}
                }});

                // Performance rating chart
                destroyChart('chartPerf');
                const depts = [...new Set(data.map(d => d.Department))];
                const deptPerfs = depts.map(d => {{
                    const sub = data.filter(x => x.Department === d);
                    return (sub.reduce((a, b) => a + b.PerformanceRating, 0) / sub.length).toFixed(2);
                }});

                const ctxPerf = document.getElementById('chartPerf').getContext('2d');
                chartInstances['chartPerf'] = new Chart(ctxPerf, {{
                    type: 'bar',
                    data: {{
                        labels: depts,
                        datasets: [{{
                            label: 'Avg Appraisal Score',
                            data: deptPerfs,
                            backgroundColor: '#10b981'
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            x: {{ ticks: {{ color: '#cbd5e1' }}, grid: {{ display: false }} }},
                            y: {{ ticks: {{ color: '#94a3b8' }}, min: 2.5, max: 4.0, grid: {{ color: '#334155' }} }}
                        }},
                        plugins: {{ legend: {{ display: false }} }}
                    }}
                }});
            }}
        }}

        // Initial Load
        window.onload = function() {{
            updateKPIs(RAW_DATA);
            renderCharts();
        }};
    </script>
</body>
</html>
"""
    with open('outputs/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    # Also write index.html at root for instant GitHub Pages hosting!
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("Generated outputs/dashboard.html and index.html successfully.")

if __name__ == '__main__':
    build_dashboard()
