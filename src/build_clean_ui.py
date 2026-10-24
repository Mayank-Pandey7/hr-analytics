"""
Builds an ultra-clean, modern, executive-friendly UI for index.html & outputs/dashboard.html.
Design Philosophy:
- Clean, bright corporate aesthetic (Light mode with soft slate accents, like Workday/Visier/Power BI)
- Clickable pill filters (1-click, no confusing dropdowns)
- Clear story flow: "Snapshot" -> "Why are they leaving?" -> "Action Plan" -> "Employee Explorer"
- Self-explanatory chart annotations and plain-English takeaways
- Searchable live employee table
"""

import json
import os
import pandas as pd

def build_clean_dashboard():
    df = pd.read_csv('data/processed/fact_hr_analytics.csv')

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
    <title>HR Analytics & Retention Intelligence</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: #f8fafc;
            color: #0f172a;
        }}
        .filter-btn-active {{
            background-color: #2563eb;
            color: #ffffff;
            box-shadow: 0 1px 3px rgba(37, 99, 235, 0.3);
        }}
        .filter-btn-inactive {{
            background-color: #ffffff;
            color: #64748b;
            border: 1px solid #e2e8f0;
        }}
        .filter-btn-inactive:hover {{
            background-color: #f1f5f9;
            color: #1e293b;
        }}
        .card {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
            border-radius: 16px;
        }}
    </style>
</head>
<body class="min-h-screen bg-slate-50 text-slate-800 antialiased">

    <!-- Top Clean Brand Navigation -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-40">
        <div class="max-w-7xl mx-auto px-6 py-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center text-white font-extrabold shadow-sm">
                    HR
                </div>
                <div>
                    <div class="flex items-center gap-2">
                        <h1 class="text-lg font-bold text-slate-900 tracking-tight">Workforce Retention Intelligence</h1>
                        <span class="text-[11px] font-semibold bg-emerald-50 text-emerald-700 px-2.5 py-0.5 rounded-full border border-emerald-200">Live Executive Report</span>
                    </div>
                    <p class="text-xs text-slate-500">Diagnostic study across 326 employees in Sales, R&D, and HR</p>
                </div>
            </div>

            <!-- Quick Jump Navigation -->
            <div class="flex items-center space-x-2 text-xs font-semibold">
                <a href="#section-kpis" class="px-3 py-1.5 rounded-lg text-slate-600 hover:bg-slate-100 transition">Overview</a>
                <a href="#section-drivers" class="px-3 py-1.5 rounded-lg text-slate-600 hover:bg-slate-100 transition">Key Drivers</a>
                <a href="#section-actions" class="px-3 py-1.5 rounded-lg text-slate-600 hover:bg-slate-100 transition">Action Plan</a>
                <a href="#section-employees" class="px-3 py-1.5 rounded-lg bg-blue-50 text-blue-700 hover:bg-blue-100 transition font-bold">Employee Directory</a>
            </div>
        </div>
    </header>

    <!-- Interactive Filter Toolbar (Simple 1-Click Pill Buttons) -->
    <section class="bg-white border-b border-slate-200 py-3 shadow-xs">
        <div class="max-w-7xl mx-auto px-6 flex flex-wrap items-center justify-between gap-4">
            
            <!-- Department Filter Pills -->
            <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-slate-400 uppercase tracking-wider mr-1">Department:</span>
                <div class="inline-flex rounded-lg p-1 bg-slate-100 border border-slate-200 text-xs">
                    <button onclick="setDept('ALL', this)" class="dept-btn filter-btn-active px-3 py-1 rounded-md font-semibold transition">All (326)</button>
                    <button onclick="setDept('Research & Development', this)" class="dept-btn filter-btn-inactive px-3 py-1 rounded-md font-medium transition">R&D (217)</button>
                    <button onclick="setDept('Sales', this)" class="dept-btn filter-btn-inactive px-3 py-1 rounded-md font-medium transition">Sales (96)</button>
                    <button onclick="setDept('Human Resources', this)" class="dept-btn filter-btn-inactive px-3 py-1 rounded-md font-medium transition">HR (13)</button>
                </div>
            </div>

            <!-- Overtime Filter Pills -->
            <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-slate-400 uppercase tracking-wider mr-1">Workload:</span>
                <div class="inline-flex rounded-lg p-1 bg-slate-100 border border-slate-200 text-xs">
                    <button onclick="setOT('ALL', this)" class="ot-btn filter-btn-active px-3 py-1 rounded-md font-semibold transition">All Staff</button>
                    <button onclick="setOT('Yes', this)" class="ot-btn filter-btn-inactive px-3 py-1 rounded-md font-medium transition text-rose-600">Overtime Only ⚠️</button>
                    <button onclick="setOT('No', this)" class="ot-btn filter-btn-inactive px-3 py-1 rounded-md font-medium transition">Standard Hours</button>
                </div>
            </div>

            <!-- Reset Button -->
            <div>
                <button onclick="resetAllFilters()" class="text-xs text-slate-500 hover:text-slate-800 font-semibold underline underline-offset-4">
                    Reset All Filters
                </button>
            </div>
        </div>
    </section>

    <!-- Main Content Container -->
    <main class="max-w-7xl mx-auto px-6 py-8 space-y-10">

        <!-- ================= SECTION 1: EXECUTIVE KPIS ================= -->
        <section id="section-kpis" class="space-y-4">
            <div>
                <h2 class="text-base font-extrabold text-slate-900 tracking-tight">1. Executive Overview & Health Metrics</h2>
                <p class="text-xs text-slate-500">Current workforce population benchmarks reflecting applied filters</p>
            </div>

            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                
                <!-- KPI 1: Headcount -->
                <div class="card p-5">
                    <div class="flex items-center justify-between text-slate-400 text-xs font-semibold">
                        <span>Workforce Size</span>
                        <span class="text-lg">👥</span>
                    </div>
                    <div class="mt-2 flex items-baseline gap-2">
                        <span id="kpiTotal" class="text-3xl font-extrabold text-slate-900">326</span>
                        <span class="text-xs text-slate-500">Total Staff</span>
                    </div>
                    <p id="kpiActiveDetail" class="text-xs text-emerald-600 font-semibold mt-2">
                        235 active employees currently retained
                    </p>
                </div>

                <!-- KPI 2: Attrition Rate -->
                <div class="card p-5 border-l-4 border-l-rose-500">
                    <div class="flex items-center justify-between text-slate-400 text-xs font-semibold">
                        <span>Overall Attrition Rate</span>
                        <span class="text-lg">🚪</span>
                    </div>
                    <div class="mt-2 flex items-baseline gap-2">
                        <span id="kpiRate" class="text-3xl font-extrabold text-rose-600">27.9%</span>
                        <span class="text-xs font-semibold px-2 py-0.5 rounded bg-rose-100 text-rose-700">Above Target</span>
                    </div>
                    <p id="kpiDepartedDetail" class="text-xs text-slate-500 mt-2">
                        91 total departures recorded
                    </p>
                </div>

                <!-- KPI 3: Compensation -->
                <div class="card p-5">
                    <div class="flex items-center justify-between text-slate-400 text-xs font-semibold">
                        <span>Average Monthly Salary</span>
                        <span class="text-lg">💵</span>
                    </div>
                    <div class="mt-2 flex items-baseline gap-2">
                        <span id="kpiSalary" class="text-3xl font-extrabold text-slate-900">$3,692</span>
                        <span class="text-xs text-slate-500">/ mo</span>
                    </div>
                    <p class="text-xs text-slate-500 mt-2">
                        Annual average: <strong id="kpiAnnual">$44,308</strong>
                    </p>
                </div>

                <!-- KPI 4: Overtime Exposure -->
                <div class="card p-5">
                    <div class="flex items-center justify-between text-slate-400 text-xs font-semibold">
                        <span>Overtime Workload</span>
                        <span class="text-lg">⏱️</span>
                    </div>
                    <div class="mt-2 flex items-baseline gap-2">
                        <span id="kpiOvertime" class="text-3xl font-extrabold text-amber-600">28.8%</span>
                        <span class="text-xs text-slate-500">of workforce</span>
                    </div>
                    <p id="kpiOtDetail" class="text-xs text-slate-500 mt-2">
                        94 employees on regular overtime
                    </p>
                </div>

            </div>
        </section>

        <!-- ================= SECTION 2: THE 3 CORE FINDINGS ("WHY ARE THEY LEAVING?") ================= -->
        <section id="section-drivers" class="space-y-4">
            <div>
                <h2 class="text-base font-extrabold text-slate-900 tracking-tight">2. Root Cause Diagnostic: Why Are Employees Leaving?</h2>
                <p class="text-xs text-slate-500">Empirical findings derived from statistical hypothesis tests and regression analysis</p>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

                <!-- Driver Card 1: Overtime Multiplier -->
                <div class="card p-5 flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-3">
                            <span class="text-[11px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-rose-100 text-rose-800">Primary Driver</span>
                            <span class="text-xs font-semibold text-slate-400">p &lt; 0.0001</span>
                        </div>
                        <h3 class="text-sm font-bold text-slate-900">Overtime Multiplies Attrition by 3.4x</h3>
                        <p class="text-xs text-slate-500 mt-1 leading-relaxed">
                            Staff assigned to regular overtime leave at a rate of <strong>56.4%</strong>, compared to just <strong>16.4%</strong> for standard-hour staff.
                        </p>
                        <div class="h-44 mt-3">
                            <canvas id="chartOvertimeSimple"></canvas>
                        </div>
                    </div>
                    <div class="pt-3 border-t border-slate-100 text-[11px] text-slate-600 font-medium">
                        💡 <strong>Takeaway:</strong> Overtime is an operational burnout trigger, not an isolated preference.
                    </div>
                </div>

                <!-- Driver Card 2: Compensation Gap -->
                <div class="card p-5 flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-3">
                            <span class="text-[11px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-amber-100 text-amber-800">Compensation Factor</span>
                            <span class="text-xs font-semibold text-slate-400">p &lt; 0.0001</span>
                        </div>
                        <h3 class="text-sm font-bold text-slate-900">The $3,500 Salary Threshold</h3>
                        <p class="text-xs text-slate-500 mt-1 leading-relaxed">
                            Employees earning under \$3,500/month experience <strong>41.7% attrition</strong>. Turnover drops to <strong>6.1%</strong> for salaries over \$7,000.
                        </p>
                        <div class="h-44 mt-3">
                            <canvas id="chartSalarySimple"></canvas>
                        </div>
                    </div>
                    <div class="pt-3 border-t border-slate-100 text-[11px] text-slate-600 font-medium">
                        💡 <strong>Takeaway:</strong> Median leaver salary is \$2,515 vs \$3,375 for retained staff (\$860 gap).
                    </div>
                </div>

                <!-- Driver Card 3: Department Vulnerability -->
                <div class="card p-5 flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-3">
                            <span class="text-[11px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-blue-100 text-blue-800">Department Risk</span>
                            <span class="text-xs font-semibold text-slate-400">N = 326</span>
                        </div>
                        <h3 class="text-sm font-bold text-slate-900">HR & Sales Face Steepest Departures</h3>
                        <p class="text-xs text-slate-500 mt-1 leading-relaxed">
                            Human Resources suffered <strong>46.2% attrition</strong>, while Sales lost <strong>31.3%</strong>. R&D had the lowest relative loss (25.4%).
                        </p>
                        <div class="h-44 mt-3">
                            <canvas id="chartDeptSimple"></canvas>
                        </div>
                    </div>
                    <div class="pt-3 border-t border-slate-100 text-[11px] text-slate-600 font-medium">
                        💡 <strong>Takeaway:</strong> HR is the lowest-paid division (\$3,070 avg), creating severe talent retention friction.
                    </div>
                </div>

            </div>

            <!-- Key Insight Alert Banner -->
            <div class="p-4 rounded-xl bg-blue-50 border border-blue-200 flex items-start gap-3">
                <span class="text-xl">💡</span>
                <div class="text-xs text-blue-900 leading-relaxed">
                    <strong>Critical Non-Finding:</strong> Departing staff held an average performance score of <strong>3.15 out of 4.00</strong> (identical to retained peers at 3.14), and <strong>93.4%</strong> had received a promotion in the past 3 years. This confirms the organization is <strong>losing valuable, high-performing talent to workload and compensation mismatch</strong>, not offboarding low performers.
                </div>
            </div>
        </section>

        <!-- ================= SECTION 3: STRATEGIC ACTION PLAN ================= -->
        <section id="section-actions" class="space-y-4">
            <div>
                <h2 class="text-base font-extrabold text-slate-900 tracking-tight">3. Strategic HR Recommendations & Roadmap</h2>
                <p class="text-xs text-slate-500">Four concrete policy interventions targeted at cutting attrition from 27.9% to &lt;18%</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="card p-5 border-l-4 border-l-rose-500">
                    <div class="flex items-center gap-2 mb-1">
                        <span class="text-xs font-bold text-rose-700 bg-rose-50 px-2 py-0.5 rounded border border-rose-200">Pillar 1 • Immediate (30 Days)</span>
                    </div>
                    <h4 class="text-sm font-bold text-slate-900 mt-1">Cap Overtime Hours & Provide Comp-Off</h4>
                    <p class="text-xs text-slate-600 mt-1.5 leading-relaxed">
                        Institute an 8-hour weekly overtime cap per worker in laboratory and sales divisions. Provide 1:1 compensatory rest days within 30 days of overtime to eliminate chronic fatigue.
                    </p>
                </div>

                <div class="card p-5 border-l-4 border-l-amber-500">
                    <div class="flex items-center gap-2 mb-1">
                        <span class="text-xs font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">Pillar 2 • Medium Term (60 Days)</span>
                    </div>
                    <h4 class="text-sm font-bold text-slate-900 mt-1">Benchmark Entry-Level Salaries to $3,200+</h4>
                    <p class="text-xs text-slate-600 mt-1.5 leading-relaxed">
                        Adjust starting base pay for Sales Representatives (avg \$2,580) and Lab Techs (avg \$2,955) to regional market median (\$3,200–\$3,500) to stop entry-tier compensation flight.
                    </p>
                </div>

                <div class="card p-5 border-l-4 border-l-blue-500">
                    <div class="flex items-center gap-2 mb-1">
                        <span class="text-xs font-bold text-blue-700 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">Pillar 3 • 60 Days</span>
                    </div>
                    <h4 class="text-sm font-bold text-slate-900 mt-1">First-Year "Flight-Risk" Mentorship</h4>
                    <p class="text-xs text-slate-600 mt-1.5 leading-relaxed">
                        46.2% of staff leave in Year 1. Establish 30-60-90 day milestone check-ins and pair new hires under 25 with mentors having 5+ years of tenure.
                    </p>
                </div>

                <div class="card p-5 border-l-4 border-l-emerald-500">
                    <div class="flex items-center gap-2 mb-1">
                        <span class="text-xs font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">Pillar 4 • Immediate</span>
                    </div>
                    <h4 class="text-sm font-bold text-slate-900 mt-1">HR Division Tooling & Parity Review</h4>
                    <p class="text-xs text-slate-600 mt-1.5 leading-relaxed">
                        Automate repetitive HR administrative paperwork to reduce burnout, and bring HR specialist salaries into parity with cross-departmental peers.
                    </p>
                </div>
            </div>
        </section>

        <!-- ================= SECTION 4: EMPLOYEE DIRECTORY & EXPLORER ================= -->
        <section id="section-employees" class="space-y-4">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div>
                    <h2 class="text-base font-extrabold text-slate-900 tracking-tight">4. Interactive Employee Explorer</h2>
                    <p class="text-xs text-slate-500">Browse individual employee records, filter by keyword, and inspect attributes</p>
                </div>
                <div class="w-full sm:w-72">
                    <input type="text" id="searchInput" oninput="searchEmployees()" placeholder="Search by ID, role, department..."
                           class="w-full bg-white border border-slate-300 rounded-lg px-3 py-1.5 text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500">
                </div>
            </div>

            <!-- Table Container -->
            <div class="card overflow-hidden">
                <div class="overflow-x-auto max-h-96">
                    <table class="w-full text-left text-xs">
                        <thead class="bg-slate-100 text-slate-600 font-bold uppercase tracking-wider sticky top-0 border-b border-slate-200">
                            <tr>
                                <th class="p-3">Employee ID</th>
                                <th class="p-3">Department</th>
                                <th class="p-3">Job Role</th>
                                <th class="p-3">Age / Gender</th>
                                <th class="p-3">Monthly Salary</th>
                                <th class="p-3">Tenure</th>
                                <th class="p-3">Overtime</th>
                                <th class="p-3">Status</th>
                            </tr>
                        </thead>
                        <tbody id="employeeTableBody" class="divide-y divide-slate-100 font-medium">
                            <!-- Populated via JS -->
                        </tbody>
                    </table>
                </div>
                <div class="p-3 bg-slate-50 border-t border-slate-200 text-[11px] text-slate-500 flex justify-between items-center">
                    <span id="tableRecordCount">Showing 326 of 326 records</span>
                    <span>Click any row to review details</span>
                </div>
            </div>
        </section>

    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-slate-200 py-6 text-center text-xs text-slate-500">
        <p class="font-semibold text-slate-700">HR Analytics & Retention Intelligence Project</p>
        <p class="text-[11px] text-slate-400 mt-1">Built with Python, SQL, and Power BI | Source Code Available on GitHub</p>
    </footer>

    <!-- Client-side Logic Script -->
    <script>
        const ALL_DATA = {records_json};
        let currentDept = 'ALL';
        let currentOT = 'ALL';
        let charts = {{}};

        function setDept(dept, btn) {{
            currentDept = dept;
            document.querySelectorAll('.dept-btn').forEach(b => {{
                b.className = 'dept-btn filter-btn-inactive px-3 py-1 rounded-md font-medium transition';
            }});
            btn.className = 'dept-btn filter-btn-active px-3 py-1 rounded-md font-semibold transition';
            refreshAll();
        }}

        function setOT(ot, btn) {{
            currentOT = ot;
            document.querySelectorAll('.ot-btn').forEach(b => {{
                b.className = 'ot-btn filter-btn-inactive px-3 py-1 rounded-md font-medium transition';
            }});
            btn.className = 'ot-btn filter-btn-active px-3 py-1 rounded-md font-semibold transition';
            refreshAll();
        }}

        function resetAllFilters() {{
            currentDept = 'ALL';
            currentOT = 'ALL';
            document.querySelectorAll('.dept-btn').forEach((b, i) => {{
                b.className = (i === 0) ? 'dept-btn filter-btn-active px-3 py-1 rounded-md font-semibold transition' : 'dept-btn filter-btn-inactive px-3 py-1 rounded-md font-medium transition';
            }});
            document.querySelectorAll('.ot-btn').forEach((b, i) => {{
                b.className = (i === 0) ? 'ot-btn filter-btn-active px-3 py-1 rounded-md font-semibold transition' : 'ot-btn filter-btn-inactive px-3 py-1 rounded-md font-medium transition';
            }});
            document.getElementById('searchInput').value = '';
            refreshAll();
        }}

        function getFilteredRecords() {{
            return ALL_DATA.filter(row => {{
                if (currentDept !== 'ALL' && row.Department !== currentDept) return false;
                if (currentOT !== 'ALL' && row.Overtime !== currentOT) return false;
                return true;
            }});
        }}

        function updateScorecards(data) {{
            const total = data.length;
            if (total === 0) {{
                document.getElementById('kpiTotal').innerText = '0';
                document.getElementById('kpiRate').innerText = '0.0%';
                document.getElementById('kpiSalary').innerText = '$0';
                document.getElementById('kpiOvertime').innerText = '0.0%';
                return;
            }}
            const active = data.filter(d => d.Attrition === 'No').length;
            const departed = data.filter(d => d.Attrition === 'Yes').length;
            const rate = ((departed / total) * 100).toFixed(1);
            const avgSal = Math.round(data.reduce((acc, r) => acc + r.Salary, 0) / total);
            const avgAnnual = Math.round(avgSal * 12);
            const otCount = data.filter(d => d.Overtime === 'Yes').length;
            const otPct = ((otCount / total) * 100).toFixed(1);

            document.getElementById('kpiTotal').innerText = total.toLocaleString();
            document.getElementById('kpiActiveDetail').innerText = `${{active}} active employees currently retained (${{((active/total)*100).toFixed(1)}}%)`;
            document.getElementById('kpiRate').innerText = rate + '%';
            document.getElementById('kpiDepartedDetail').innerText = `${{departed}} total departures recorded`;
            document.getElementById('kpiSalary').innerText = '$' + avgSal.toLocaleString();
            document.getElementById('kpiAnnual').innerText = '$' + avgAnnual.toLocaleString();
            document.getElementById('kpiOvertime').innerText = otPct + '%';
            document.getElementById('kpiOtDetail').innerText = `${{otCount}} employees on regular overtime`;
        }}

        function renderVisuals(data) {{
            // 1. Overtime Comparison
            if (charts.ot) charts.ot.destroy();
            const otYes = data.filter(d => d.Overtime === 'Yes');
            const otNo = data.filter(d => d.Overtime === 'No');
            const otYesRate = otYes.length ? ((otYes.filter(d => d.Attrition === 'Yes').length / otYes.length) * 100).toFixed(1) : 0;
            const otNoRate = otNo.length ? ((otNo.filter(d => d.Attrition === 'Yes').length / otNo.length) * 100).toFixed(1) : 0;

            const ctxOt = document.getElementById('chartOvertimeSimple').getContext('2d');
            charts.ot = new Chart(ctxOt, {{
                type: 'bar',
                data: {{
                    labels: ['Standard Hours', 'Overtime Staff'],
                    datasets: [{{
                        label: 'Attrition Rate (%)',
                        data: [otNoRate, otYesRate],
                        backgroundColor: ['#94a3b8', '#e11d48'],
                        borderRadius: 8
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{ max: 100, ticks: {{ callback: v => v + '%' }} }}
                    }},
                    plugins: {{ legend: {{ display: false }} }}
                }}
            }});

            // 2. Salary Band Comparison
            if (charts.sal) charts.sal.destroy();
            const bands = ['< $3,500 (Entry)', '$3,500 - $6,999 (Mid)', '$7,000 - $11,999 (Senior)', '$12,000+ (Executive)'];
            const bandRates = bands.map(b => {{
                const sub = data.filter(d => d.SalaryBand === b);
                return sub.length ? ((sub.filter(d => d.Attrition === 'Yes').length / sub.length) * 100).toFixed(1) : 0;
            }});

            const ctxSal = document.getElementById('chartSalarySimple').getContext('2d');
            charts.sal = new Chart(ctxSal, {{
                type: 'bar',
                data: {{
                    labels: ['< $3.5k', '$3.5k-$7k', '$7k-$12k', '$12k+'],
                    datasets: [{{
                        label: 'Attrition Rate (%)',
                        data: bandRates,
                        backgroundColor: ['#e11d48', '#f59e0b', '#3b82f6', '#10b981'],
                        borderRadius: 8
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{ max: 60, ticks: {{ callback: v => v + '%' }} }}
                    }},
                    plugins: {{ legend: {{ display: false }} }}
                }}
            }});

            // 3. Department Comparison
            if (charts.dept) charts.dept.destroy();
            const depts = ['Human Resources', 'Sales', 'Research & Development'];
            const deptRates = depts.map(d => {{
                const sub = data.filter(x => x.Department === d);
                return sub.length ? ((sub.filter(x => x.Attrition === 'Yes').length / sub.length) * 100).toFixed(1) : 0;
            }});

            const ctxDept = document.getElementById('chartDeptSimple').getContext('2d');
            charts.dept = new Chart(ctxDept, {{
                type: 'bar',
                data: {{
                    labels: ['HR', 'Sales', 'R&D'],
                    datasets: [{{
                        label: 'Attrition Rate (%)',
                        data: deptRates,
                        backgroundColor: ['#e11d48', '#f59e0b', '#2563eb'],
                        borderRadius: 8
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{ max: 60, ticks: {{ callback: v => v + '%' }} }}
                    }},
                    plugins: {{ legend: {{ display: false }} }}
                }}
            }});
        }}

        function populateTable(data) {{
            const tbody = document.getElementById('employeeTableBody');
            const search = document.getElementById('searchInput').value.toLowerCase().trim();

            const filtered = data.filter(d => {{
                if (!search) return true;
                return d.EmployeeID.toLowerCase().includes(search) ||
                       d.JobRole.toLowerCase().includes(search) ||
                       d.Department.toLowerCase().includes(search);
            }});

            document.getElementById('tableRecordCount').innerText = `Showing ${{filtered.length}} of ${{data.length}} records`;

            let html = '';
            filtered.slice(0, 100).forEach(emp => {{
                const isLeft = emp.Attrition === 'Yes';
                const statusBadge = isLeft
                    ? '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-100 text-rose-700">Departed</span>'
                    : '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-700">Active</span>';

                const otBadge = emp.Overtime === 'Yes'
                    ? '<span class="text-amber-600 font-bold">Yes (OT)</span>'
                    : '<span class="text-slate-400">Standard</span>';

                html += `<tr class="hover:bg-slate-50 transition cursor-pointer">
                    <td class="p-3 font-mono font-bold text-slate-900">${{emp.EmployeeID}}</td>
                    <td class="p-3 text-slate-600">${{emp.Department}}</td>
                    <td class="p-3 text-slate-800 font-medium">${{emp.JobRole}}</td>
                    <td class="p-3 text-slate-600">${{emp.Age}} yrs • ${{emp.Gender}}</td>
                    <td class="p-3 text-slate-900 font-bold">$${{emp.Salary.toLocaleString()}}</td>
                    <td class="p-3 text-slate-600">${{emp.YearsAtCompany}} yrs</td>
                    <td class="p-3">${{otBadge}}</td>
                    <td class="p-3">${{statusBadge}}</td>
                </tr>`;
            }});

            tbody.innerHTML = html || '<tr><td colspan="8" class="p-6 text-center text-slate-400">No matching employees found.</td></tr>';
        }}

        function searchEmployees() {{
            populateTable(getFilteredRecords());
        }}

        function refreshAll() {{
            const data = getFilteredRecords();
            updateScorecards(data);
            renderVisuals(data);
            populateTable(data);
        }}

        window.onload = function() {{
            refreshAll();
        }};
    </script>
</body>
</html>
"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    with open('outputs/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("Clean corporate UI built successfully into index.html and outputs/dashboard.html")

if __name__ == '__main__':
    build_clean_dashboard()
