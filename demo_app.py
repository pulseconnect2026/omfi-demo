import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="omfi - Independent Debt-Free Command Center",
    page_icon="💡",
    layout="wide"
)

# Custom Dark Theme CSS matching your brand style (Midnight background, glowing pulse accents)
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #0b132b;
        color: #ffffff;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1c2541;
        color: #ffffff;
    }
    
    /* Metric cards styling */
    .stMetric {
        background-color: #1c2541;
        padding: 18px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        border: 1px solid #48cae4;
    }
    
    /* Metric Label (e.g., Total Outstanding Debt) */
    [data-testid="stMetricLabel"] p {
        color: #94a3b8 !important;
        font-weight: 600 !important;
    }
    
    /* Metric Value Numbers (Bright White and Bold) */
    [data-testid="stMetricValue"] div, [data-testid="stMetricValue"] span {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    
    /* Hero Banner matching the Pulse aesthetic */
    .pulse-banner {
        background: linear-gradient(90deg, #1c2541 0%, #0b132b 100%);
        border-left: 5px solid #ff4d4d;
        border-right: 5px solid #00b4d8;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    }
    
    /* Dataframe table styling */
    DataFrame, .stDataFrame {
        background-color: #1c2541;
        border-radius: 8px;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #ffffff !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# Custom Hero Header
st.markdown("""
    <div class="pulse-banner">
        <h1 style="margin: 0; font-size: 2.2em; color: #ffffff;">
            omfi <span style="color: #48cae4;">COMMAND CENTER</span>
        </h1>
        <p style="font-size: 1.1em; color: #94a3b8; margin-top: 8px;">
            <span style="color: #ff4d4d; font-weight: bold;">■</span> Debt Independence &nbsp;|&nbsp; 
            <span style="color: #00b4d8; font-weight: bold;">■</span> Financial Self-Management
        </p>
        <span style="background: linear-gradient(90deg, #ff4d4d, #00b4d8); color: #ffffff; padding: 5px 16px; border-radius: 20px; font-weight: bold; font-size: 0.85em; display: inline-block; margin-top: 10px;">
            INTERACTIVE DEMO MODE
        </span>
    </div>
""", unsafe_allow_html=True)

# Sidebar Profile Selector
st.sidebar.header("⚙️ Demo Controls")
profile_type = st.sidebar.selectbox(
    "Choose Sample Financial Profile",
    ["Moderate Debt (Standard)", "High Credit Card Burden", "Starter Budget"]
)

# Load profile-specific mock data
if profile_type == "High Credit Card Burden":
    MOCK_ACCOUNTS = [
        {"name": "Platinum Visa", "balance": 8500.00, "apr": 26.99, "min_payment": 220.00},
        {"name": "Department Store Card", "balance": 2400.00, "apr": 22.99, "min_payment": 75.00},
        {"name": "Auto Loan", "balance": 14000.00, "apr": 7.50, "min_payment": 380.00},
    ]
    monthly_income = 5200.00
elif profile_type == "Starter Budget":
    MOCK_ACCOUNTS = [
        {"name": "Starter Card", "balance": 1500.00, "apr": 18.99, "min_payment": 45.00},
    ]
    monthly_income = 3800.00
else:
    MOCK_ACCOUNTS = [
        {"name": "Rewards Credit Card", "balance": 3500.00, "apr": 24.99, "min_payment": 105.00},
        {"name": "Store Card", "balance": 1200.00, "apr": 19.99, "min_payment": 45.00},
        {"name": "Personal Loan", "balance": 8500.00, "apr": 11.50, "min_payment": 210.00},
    ]
    monthly_income = 4800.00

MOCK_BILLS = [
    {"bill_name": "Electric Utility", "amount": 145.00, "due_day": 5},
    {"bill_name": "Internet Service", "amount": 85.00, "due_day": 12},
    {"bill_name": "Car Insurance", "amount": 160.00, "due_day": 20},
]

# Tabs Definition
tab_dash, tab_bills, tab_debt, tab_sim = st.tabs([
    "📊 Dashboard", 
    "📅 Pay & Bills", 
    "💳 Credit Cards & Debt", 
    "⚡ Strategy Simulator"
])

total_debt = sum(item["balance"] for item in MOCK_ACCOUNTS)
total_min_pay = sum(item["min_payment"] for item in MOCK_ACCOUNTS)
total_bills = sum(item["amount"] for item in MOCK_BILLS)
est_cash_flow = monthly_income - (total_min_pay + total_bills)

# --- TAB 1: DASHBOARD ---
with tab_dash:
    st.subheader("Financial Command Center Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Outstanding Debt", f"${total_debt:,.2f}")
    col2.metric("Monthly Min Payments", f"${total_min_pay:,.2f}")
    col3.metric("Recurring Bills", f"${total_bills:,.2f}")
    col4.metric("Est. Monthly Cash Flow", f"${est_cash_flow:,.2f}", delta="Healthy" if est_cash_flow > 500 else "Tight")

    st.markdown("---")
    c_left, c_right = st.columns(2)
    with c_left:
        st.markdown("### 📌 Active Bill Timeline")
        df_bills = pd.DataFrame(MOCK_BILLS)
        df_bills.columns = ["Bill Name", "Amount ($)", "Due Day of Month"]
        st.dataframe(df_bills, use_container_width=True, hide_index=True)
    with c_right:
        st.markdown("### 💡 Financial Health Insight")
        st.info(
            "Your debt-to-income ratio and payment schedule are tracked in real-time. "
            "Switch to the **Strategy Simulator** tab to test how extra monthly payments cut down your timeline."
        )

# --- TAB 2: PAY & BILLS ---
with tab_bills:
    st.subheader("Pay Schedule & Deficit Prevention")
    st.write(f"**Configured Income Profile:** Bi-Weekly (Total Monthly: ${monthly_income:,.2f})")
    
    if est_cash_flow > 400:
        st.success("✅ **Cash-Flow Status:** Healthy buffer detected across upcoming pay periods.")
    else:
        st.warning("⚠️ **Cash-Flow Warning:** Tight cash flow detected. Consider reallocating discretionary funds.")

    st.markdown("### Upcoming Payment Obligations")
    df_bills_full = pd.DataFrame(MOCK_BILLS)
    df_bills_full.columns = ["Bill Name", "Amount", "Due Day"]
    st.dataframe(df_bills_full, use_container_width=True, hide_index=True)

# --- TAB 3: DEBT OVERVIEW ---
with tab_debt:
    st.subheader("Current Debt Portfolio")
    df_debt = pd.DataFrame(MOCK_ACCOUNTS)
    df_debt.columns = ["Account Name", "Current Balance ($)", "APR (%)", "Min Payment ($)"]
    st.dataframe(df_debt, use_container_width=True, hide_index=True)

# --- TAB 4: STRATEGY SIMULATOR ---
with tab_sim:
    st.subheader("⚡ Debt Snowball vs. Avalanche Simulator")
    st.write("Test out custom extra monthly contributions to see your projected debt-free milestone.")

    extra_pay = st.slider("Extra Monthly Contribution ($)", min_value=0, max_value=1000, value=300, step=50)
    strategy = st.radio("Payoff Algorithm", ["Snowball (Lowest Balance First)", "Avalanche (Highest APR First)"], horizontal=True)

    # Simulation metrics
    months_baseline = max(1, int(total_debt / (total_min_pay if total_min_pay > 0 else 1)))
    months_accelerated = max(1, int(total_debt / (total_min_pay + extra_pay)))
    time_saved = max(0, months_baseline - months_accelerated)
    interest_saved = time_saved * (total_debt * 0.18 / 12)

    c1, c2, c3 = st.columns(3)
    c1.metric("Standard Payoff Timeline", f"{months_baseline} Months")
    c2.metric("Accelerated Timeline", f"{months_accelerated} Months", delta=f"-{time_saved} Months", delta_color="normal")
    c3.metric("Est. Interest Saved", f"${max(0, interest_saved):,.2f}")

    # Visual Chart
    months_range = list(range(0, months_baseline + 1))
    baseline_curve = [max(0, total_debt - (m * total_min_pay)) for m in months_range]
    accelerated_curve = [max(0, total_debt - (m * (total_min_pay + extra_pay))) for m in months_range]

    chart_data = pd.DataFrame({
        "Month": months_range,
        "Minimum Payments Only": baseline_curve,
        "With Extra Payment": accelerated_curve
    }).set_index("Month")

    st.line_chart(chart_data)

# Footer CTA for Site Integration
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #94a3b8; padding: 10px;'>
        <p>Want to unlock automated bank syncing, custom payment schedules, and permanent cloud backup? 
        <br><b><a href="#" target="_self" style="color: #48cae4; text-decoration: none;">Create your account today</a></b></p>
    </div>
    """, 
    unsafe_allow_html=True
)