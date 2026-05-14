import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import urllib.parse  
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. SETUP & CONFIGURATION
# ==========================================
DB_USER = "root"
DB_PASSWORD = urllib.parse.quote_plus("Kusumahara@123")  
DB_HOST = "localhost"
DB_NAME = "healthcare_db"
DB_TABLE = "healthcare_dataset"  

connection_string = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(connection_string)

try:
    # ==========================================
    # 2. DATA EXTRACTION
    # ==========================================
    print("--- PHASE 1: DATA EXTRACTION ---")
    df = pd.read_sql(f"SELECT * FROM {DB_TABLE}", engine)
    print(f"Success: Loaded {df.shape[0]} patient records from MySQL database.")

    # ==========================================
    # 3. DATA CLEANING & STANDARDIZATION
    # ==========================================
    print("\n--- PHASE 2: DATA CLEANING & STANDARDIZATION ---")
    df.columns = df.columns.str.replace(' ', '_').str.strip()
    print("System: Normalized column headers with underscores for strict consistency.")
    print(df.columns.tolist())
    
    # Check for missing values safely
    null_summary = df.isnull().sum()
    print("System: Missing data scan complete.")

    # ==========================================
    # 4. DATA PROCESSING & ADVANCED CORE METRICS
    # ==========================================
    print("\n--- PHASE 3: CALCULATING CORE FINANCIAL METRICS ---")
    
    # Base Financial Calculations
    avg_bill = np.round(df['Billing_Amount'].mean(), 2) if 'Billing_Amount' in df.columns else 0
    total_bill = np.round(df['Billing_Amount'].sum(), 2) if 'Billing_Amount' in df.columns else 0

    # Operational Calculations: Length of Stay & Financial Efficiency Per Day
    has_dates = all(col in df.columns for col in ['Discharge_Date', 'Date_of_Admission', 'Billing_Amount'])
    print(f"Debug: has_dates = {has_dates}")
    print(f"Debug: Required columns present: {[col in df.columns for col in ['Discharge_Date', 'Date_of_Admission', 'Billing_Amount']]}")
    if has_dates:
        df['Date_of_Admission'] = pd.to_datetime(df['Date_of_Admission'])
        df['Discharge_Date'] = pd.to_datetime(df['Discharge_Date'])
        df['Length_of_Stay'] = (df['Discharge_Date'] - df['Date_of_Admission']).dt.days
        df['Length_of_Stay'] = df['Length_of_Stay'].replace(0, 1) # Prevent zero division
        df['Revenue_Per_Day'] = df['Billing_Amount'] / df['Length_of_Stay']

    # Portfolio Risk Segregation (Claims > $30k)
    if 'Billing_Amount' in df.columns:
        high_value_claims = df[df['Billing_Amount'] > 30000]
        total_at_risk = high_value_claims['Billing_Amount'].sum()
        count_at_risk = high_value_claims.shape[0]
        percentage_at_risk = (total_at_risk / total_bill) * 100

    # ==========================================
    # 5. FINAL REPORTS & PERFORMANCE OUTPUTS
    # ==========================================
    print("\n--- PHASE 4: EXECUTIVE REPORTING GENERATION ---")
    print(f"Total Revenue Managed: ${total_bill:,}")
    print(f"Average Invoice Cost: ${avg_bill:,}")

    if 'Admission_Type' in df.columns and 'Billing_Amount' in df.columns:
        print("\n[Report A] Revenue Performance by Admission Type:")
        admission_summary = df.groupby('Admission_Type')['Billing_Amount'].agg(['count', 'sum', 'mean']).round(2)
        admission_summary.columns = ['Total_Patients', 'Total_Revenue', 'Avg_Cost_Per_Patient']
        print(admission_summary)
            
    if 'Insurance_Provider' in df.columns and 'Billing_Amount' in df.columns:
        print("\n[Report B] Financial Yield by Insurance Provider:")
        insurance_summary = df.groupby('Insurance_Provider')['Billing_Amount'].agg(['sum', 'mean']).round(2)
        insurance_summary.columns = ['Total_Payout', 'Avg_Payout']
        print(insurance_summary.sort_values(by='Total_Payout', ascending=False))

    if 'Medical_Condition' in df.columns and 'Billing_Amount' in df.columns:
        print("\n[Report C] Average Cost Matrix per Medical Condition (Top 5):")
        condition_summary = df.groupby('Medical_Condition')['Billing_Amount'].mean().round(2)
        print(condition_summary.sort_values(ascending=False).head(5))

    if has_dates:
        print("\n[Advanced Report D] Bed Turnover Efficiency (Top 5 Conditions by Rev/Day):")
        los_financials = df.groupby('Medical_Condition').agg(
            Avg_LOS=('Length_of_Stay', 'mean'),
            Avg_Revenue_Per_Day=('Revenue_Per_Day', 'mean')
        ).round(2)
        print(los_financials.sort_values(by='Avg_Revenue_Per_Day', ascending=False).head(5))

    if all(col in df.columns for col in ['Insurance_Provider', 'Medical_Condition', 'Billing_Amount']):
        print("\n[Advanced Report E] Top 5 High-Yield Payer-Condition Intersections:")
        matrix = df.groupby(['Insurance_Provider', 'Medical_Condition'])['Billing_Amount'].mean().reset_index()
        matrix.columns = ['Insurance_Provider', 'Medical_Condition', 'Avg_Claim_Value']
        print(matrix.sort_values(by='Avg_Claim_Value', ascending=False).head(5).to_string(index=False))

    if 'Billing_Amount' in df.columns:
        print("\n[Advanced Report F] Revenue Portfolio Risk Segmentation:")
        print(f" -> High-Value Claims (> $30k) Awaiting Audits: {count_at_risk} accounts")
        print(f" -> Financial Volume Out for Collection: ${total_at_risk:,.2f}")
        print(f" -> Percentage of Entire Hospital Portfolio at Risk: {percentage_at_risk:.2f}%")

    print("\nData Integrity Scan: Missing values per database field:")
    print(null_summary)

    # ==========================================
    # 6. VISUALIZATION EXPORT (THE FINALE)
    # ==========================================
    print("\n--- PHASE 5: EXPORTING VISUALIZATION DASHBOARD ---")
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Plot 1: Insurance Performance
    if 'Insurance_Provider' in df.columns and 'Billing_Amount' in df.columns:
        sns.barplot(data=df, x='Insurance_Provider', y='Billing_Amount', estimator=sum, errorbar=None, palette='Blues_r', ax=axes[0])
        axes[0].set_title('Total Revenue by Insurance Provider', fontsize=12, fontweight='bold')
        axes[0].set_xlabel('Insurance Provider')
        axes[0].set_ylabel('Total Revenue ($)')
        axes[0].get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

    # Plot 2: Condition Cost Breakdown
    if 'Medical_Condition' in df.columns and 'Billing_Amount' in df.columns:
        top_conditions = df.groupby('Medical_Condition')['Billing_Amount'].mean().reset_index().sort_values(by='Billing_Amount', ascending=False)
        sns.barplot(data=top_conditions, y='Medical_Condition', x='Billing_Amount', palette='crest', ax=axes[1])
        axes[1].set_title('Average Treatment Cost by Condition', fontsize=12, fontweight='bold')
        axes[1].set_xlabel('Average Cost ($)')
        axes[1].set_ylabel('Medical Condition')

    plt.tight_layout()
    output_filename = "healthcare_financial_dashboard.png"
    plt.savefig(output_filename, dpi=300)
    print(f"Success! Final executive visualization exported to: '{output_filename}'")
    print("\n*** DATA PIPELINE EXECUTION COMPLETE ***")

except Exception as error_message:
    print("\n--- SYSTEM CRASH: PROCESS TERMINATED ---")
    print(f"Error Details: {error_message}")