"""
HR Analytics Chart Generation and Interpretable Machine Learning Module
Generates publication-quality charts in outputs/charts/ and evaluates
an interpretable attrition prediction model (Logistic Regression & Random Forest).
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, roc_curve, confusion_matrix

# Set global aesthetic style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9

PRIMARY_COLOR = '#1f77b4'
ALERT_COLOR = '#d62728'
SUCCESS_COLOR = '#2ca02c'
NEUTRAL_COLOR = '#7f7f7f'

def create_all_visualizations(data_path='data/processed/fact_hr_analytics.csv',
                             output_dir='outputs/charts'):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} records for visualization...")

    # -------------------------------------------------------------
    # Chart 1: Department Headcount & Attrition Rate
    # -------------------------------------------------------------
    dept_stats = df.groupby('Department').agg(
        Total=('EmployeeID', 'count'),
        Departed=('AttritionNumeric', 'sum')
    ).reset_index()
    dept_stats['AttritionRate'] = (dept_stats['Departed'] / dept_stats['Total']) * 100
    dept_stats = dept_stats.sort_values('AttritionRate', ascending=False)

    fig, ax1 = plt.subplots(figsize=(8, 5))
    bars = ax1.bar(dept_stats['Department'], dept_stats['Total'], color='#2b5c8f', width=0.45, label='Total Headcount')
    ax1.set_ylabel('Total Employees', color='#2b5c8f', fontweight='bold')
    ax1.tick_params(axis='y', labelcolor='#2b5c8f')
    ax1.set_ylim(0, max(dept_stats['Total']) * 1.2)

    ax2 = ax1.twinx()
    line = ax2.plot(dept_stats['Department'], dept_stats['AttritionRate'], color=ALERT_COLOR, marker='o', linewidth=2.5, markersize=8, label='Attrition Rate (%)')
    ax2.set_ylabel('Attrition Rate (%)', color=ALERT_COLOR, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=ALERT_COLOR)
    ax2.set_ylim(0, max(dept_stats['AttritionRate']) * 1.3)
    ax2.grid(False)

    for i, txt in enumerate(dept_stats['AttritionRate']):
        ax2.annotate(f"{txt:.1f}%", (i, txt + 1.5), ha='center', color=ALERT_COLOR, fontweight='bold')
    for bar in bars:
        h = bar.get_height()
        ax1.annotate(f"{int(h)}", (bar.get_x() + bar.get_width() / 2, h + 3), ha='center', color='#2b5c8f', fontweight='bold')

    plt.title('Department Workforce Headcount vs Attrition Rate', pad=15)
    plt.tight_layout()
    fig1_path = os.path.join(output_dir, '01_headcount_and_attrition_by_dept.png')
    plt.savefig(fig1_path, dpi=300)
    plt.close()
    print(f"Saved: {fig1_path}")

    # -------------------------------------------------------------
    # Chart 2: Attrition Rate by Job Role
    # -------------------------------------------------------------
    role_stats = df.groupby('JobRole').agg(
        Total=('EmployeeID', 'count'),
        Departed=('AttritionNumeric', 'sum')
    ).reset_index()
    role_stats['AttritionRate'] = (role_stats['Departed'] / role_stats['Total']) * 100
    role_stats = role_stats.sort_values('AttritionRate', ascending=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = [ALERT_COLOR if r >= 30 else PRIMARY_COLOR for r in role_stats['AttritionRate']]
    bars = ax.barh(role_stats['JobRole'], role_stats['AttritionRate'], color=colors, height=0.6)
    ax.axvline(df['AttritionNumeric'].mean() * 100, color='black', linestyle='--', linewidth=1.5, label=f"Org Avg: {df['AttritionNumeric'].mean()*100:.1f}%")
    
    for bar in bars:
        w = bar.get_width()
        ax.annotate(f" {w:.1f}%", (w, bar.get_y() + bar.get_height() / 2), va='center', fontweight='bold', fontsize=9)
        
    ax.set_xlabel('Attrition Rate (%)')
    ax.set_title('Attrition Rate by Job Role (Benchmark vs Org Average)', pad=15)
    ax.legend(loc='lower right')
    plt.tight_layout()
    fig2_path = os.path.join(output_dir, '02_attrition_by_job_role.png')
    plt.savefig(fig2_path, dpi=300)
    plt.close()
    print(f"Saved: {fig2_path}")

    # -------------------------------------------------------------
    # Chart 3: Overtime Impact on Attrition
    # -------------------------------------------------------------
    ot_df = df.groupby(['Overtime', 'Attrition']).size().unstack(fill_value=0)
    ot_pct = ot_df.div(ot_df.sum(axis=1), axis=0) * 100

    fig, ax = plt.subplots(figsize=(7, 5))
    x = np.arange(len(ot_pct))
    width = 0.35
    ax.bar(x - width/2, ot_pct['No'], width, label='Retained (No)', color='#4c72b0')
    ax.bar(x + width/2, ot_pct['Yes'], width, label='Attrited (Yes)', color=ALERT_COLOR)

    ax.set_xticks(x)
    ax.set_xticklabels([f"No Overtime\n(N={ot_df.loc['No'].sum()})", f"Overtime Worker\n(N={ot_df.loc['Yes'].sum()})"])
    ax.set_ylabel('Percentage (%)')
    ax.set_title('Attrition Comparison: Overtime vs Non-Overtime Employees', pad=15)
    ax.set_ylim(0, 100)
    ax.legend(loc='upper right')

    for i in x:
        ax.annotate(f"{ot_pct['No'].iloc[i]:.1f}%", (i - width/2, ot_pct['No'].iloc[i] + 2), ha='center', fontweight='bold')
        ax.annotate(f"{ot_pct['Yes'].iloc[i]:.1f}%", (i + width/2, ot_pct['Yes'].iloc[i] + 2), ha='center', fontweight='bold', color=ALERT_COLOR)

    plt.tight_layout()
    fig3_path = os.path.join(output_dir, '03_overtime_impact_on_attrition.png')
    plt.savefig(fig3_path, dpi=300)
    plt.close()
    print(f"Saved: {fig3_path}")

    # -------------------------------------------------------------
    # Chart 4: Monthly Salary Distribution by Attrition Status
    # -------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))
    sns.boxplot(x='Attrition', y='Salary', data=df, palette=['#4c72b0', ALERT_COLOR], ax=ax1, width=0.4)
    ax1.set_title('Salary Box Plot by Attrition')
    ax1.set_ylabel('Monthly Income ($)')
    ax1.set_xlabel('Attrition')

    sns.kdeplot(df[df['Attrition']=='No']['Salary'], fill=True, color='#4c72b0', label='Retained', ax=ax2, alpha=0.4)
    sns.kdeplot(df[df['Attrition']=='Yes']['Salary'], fill=True, color=ALERT_COLOR, label='Attrited', ax=ax2, alpha=0.4)
    ax2.set_title('Salary Density Distribution')
    ax2.set_xlabel('Monthly Income ($)')
    ax2.set_ylabel('Density')
    ax2.legend()

    plt.tight_layout()
    fig4_path = os.path.join(output_dir, '04_salary_distribution_by_attrition.png')
    plt.savefig(fig4_path, dpi=300)
    plt.close()
    print(f"Saved: {fig4_path}")

    # -------------------------------------------------------------
    # Chart 5: Correlation Heatmap
    # -------------------------------------------------------------
    num_cols = ['Age', 'Salary', 'YearsOfExperience', 'YearsAtCompany', 'AttendanceRate',
                'AbsenceDays', 'JobSatisfaction', 'PerformanceRating', 'PromotionHistory',
                'WorkLifeBalance', 'TrainingHours', 'AttritionNumeric']
    corr = df[num_cols].corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', vmin=-0.6, vmax=0.6, center=0,
                square=True, linewidths=0.5, cbar_kws={'shrink': 0.8}, ax=ax)
    ax.set_title('Correlation Matrix of Quantitative HR Metrics', pad=15)
    plt.tight_layout()
    fig5_path = os.path.join(output_dir, '05_correlation_heatmap.png')
    plt.savefig(fig5_path, dpi=300)
    plt.close()
    print(f"Saved: {fig5_path}")

    # -------------------------------------------------------------
    # Chart 6: Job Satisfaction & Work-Life Balance Matrix
    # -------------------------------------------------------------
    pivot_matrix = df.pivot_table(index='JobSatisfactionLabel', columns='WorkLifeBalanceLabel',
                                  values='AttritionNumeric', aggfunc=lambda x: np.mean(x)*100)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(pivot_matrix, annot=True, fmt='.1f', cmap='YlOrRd', ax=ax, cbar_kws={'label': 'Attrition Rate (%)'})
    ax.set_title('Attrition Rate Risk Matrix: Job Satisfaction vs Work-Life Balance (%)', pad=15)
    ax.set_xlabel('Work-Life Balance Tier')
    ax.set_ylabel('Job Satisfaction Tier')
    plt.tight_layout()
    fig6_path = os.path.join(output_dir, '06_satisfaction_and_worklife_balance_matrix.png')
    plt.savefig(fig6_path, dpi=300)
    plt.close()
    print(f"Saved: {fig6_path}")

    # -------------------------------------------------------------
    # Chart 7: Attendance and Absenteeism Distributions
    # -------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    sns.histplot(df['AttendanceRate'], bins=15, kde=True, color='#2b5c8f', ax=ax1)
    ax1.set_title('Attendance Rate Distribution (%)')
    ax1.set_xlabel('Attendance Rate (%)')

    sns.boxplot(x='Attrition', y='AbsenceDays', data=df, palette=['#4c72b0', ALERT_COLOR], ax=ax2, width=0.4)
    ax2.set_title('Absence Days by Attrition Cohort')
    ax2.set_xlabel('Attrition')
    ax2.set_ylabel('Annual Absence Days')

    plt.tight_layout()
    fig7_path = os.path.join(output_dir, '07_attendance_absenteeism_distribution.png')
    plt.savefig(fig7_path, dpi=300)
    plt.close()
    print(f"Saved: {fig7_path}")

    return df

def train_interpretable_models(data_path='data/processed/fact_hr_analytics.csv',
                              output_dir='outputs/charts'):
    df = pd.read_csv(data_path)

    # Feature selection: avoid data leakage, focus on actionable drivers
    features_num = ['Age', 'Salary', 'YearsOfExperience', 'YearsAtCompany',
                    'AttendanceRate', 'AbsenceDays', 'JobSatisfaction',
                    'PerformanceRating', 'PromotionHistory', 'WorkLifeBalance', 'TrainingHours']
    features_cat = ['Department', 'JobRole', 'Overtime', 'MaritalStatus']

    X = df[features_num + features_cat]
    y = df['AttritionNumeric']

    # Stratified Train/Test split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), features_num),
            ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), features_cat)
        ]
    )

    # 1. Interpretable Model: Logistic Regression with L2 regularization
    log_reg = Pipeline([
        ('prep', preprocessor),
        ('clf', LogisticRegression(class_weight='balanced', random_state=42, max_iter=1000))
    ])

    log_reg.fit(X_train, y_train)
    y_pred_proba = log_reg.predict_proba(X_test)[:, 1]
    y_pred = (y_pred_proba >= 0.5).astype(int)

    roc_auc = roc_auc_score(y_test, y_pred_proba)
    report = classification_report(y_test, y_pred, target_names=['Retained', 'Attrited'], output_dict=True)

    print("\n=== INTERPRETABLE ATTRITION PREDICTION MODEL ===")
    print(f"Test Set ROC-AUC Score: {roc_auc:.3f}")
    print(f"Attrited Precision: {report['Attrited']['precision']:.2f}")
    print(f"Attrited Recall:    {report['Attrited']['recall']:.2f}")
    print(f"Attrited F1-Score:  {report['Attrited']['f1-score']:.2f}")

    # Extract feature coefficients
    ohe_names = log_reg.named_steps['prep'].named_transformers_['cat'].get_feature_names_out(features_cat)
    feature_names = features_num + list(ohe_names)
    coefs = log_reg.named_steps['clf'].coef_[0]

    coef_df = pd.DataFrame({
        'Feature': feature_names,
        'Coefficient': coefs,
        'OddsRatio': np.exp(coefs)
    }).sort_values('Coefficient', key=abs, ascending=False)

    # Save feature importances
    coef_df.to_csv('outputs/reports/model_coefficients.csv', index=False)

    # Chart 8: Top Odds Ratio Drivers
    top_coefs = pd.concat([coef_df.head(7), coef_df.tail(5)]).drop_duplicates().sort_values('Coefficient')
    fig, ax = plt.subplots(figsize=(9, 6))
    colors = [ALERT_COLOR if c > 0 else '#2ca02c' for c in top_coefs['Coefficient']]
    ax.barh(top_coefs['Feature'], top_coefs['Coefficient'], color=colors, height=0.6)
    ax.axvline(0, color='black', linestyle='--', linewidth=1)
    ax.set_xlabel('Log-Odds Coefficient (Positive = Higher Risk, Negative = Retention Factor)')
    ax.set_title('Top Statistical Drivers of Employee Attrition (Logistic Regression)', pad=15)
    plt.tight_layout()
    fig8_path = os.path.join(output_dir, '08_model_feature_importance.png')
    plt.savefig(fig8_path, dpi=300)
    plt.close()
    print(f"Saved: {fig8_path}")

    # Chart 9: ROC Curve
    fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.plot(fpr, tpr, color=PRIMARY_COLOR, linewidth=2.5, label=f'Logistic Regression (AUC = {roc_auc:.3f})')
    ax.plot([0, 1], [0, 1], color=NEUTRAL_COLOR, linestyle='--', linewidth=1.5, label='Random Chance (AUC = 0.50)')
    ax.set_xlabel('False Positive Rate (1 - Specificity)')
    ax.set_ylabel('True Positive Rate (Sensitivity / Recall)')
    ax.set_title('ROC Curve for Employee Attrition Risk Classification', pad=15)
    ax.legend(loc='lower right')
    plt.tight_layout()
    fig9_path = os.path.join(output_dir, '09_model_roc_curve.png')
    plt.savefig(fig9_path, dpi=300)
    plt.close()
    print(f"Saved: {fig9_path}")

    # Save evaluation summary table
    eval_df = pd.DataFrame([{
        'Model': 'Balanced Logistic Regression',
        'ROC_AUC': round(roc_auc, 3),
        'Precision_Attrited': round(report['Attrited']['precision'], 3),
        'Recall_Attrited': round(report['Attrited']['recall'], 3),
        'F1_Score_Attrited': round(report['Attrited']['f1-score'], 3),
        'Accuracy': round(report['accuracy'], 3)
    }])
    eval_df.to_csv('outputs/reports/model_performance_metrics.csv', index=False)
    print("Exported model metrics to outputs/reports/model_performance_metrics.csv")

if __name__ == '__main__':
    create_all_visualizations()
    train_interpretable_models()
