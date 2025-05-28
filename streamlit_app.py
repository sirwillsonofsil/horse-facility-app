import streamlit as st

st.set_page_config(page_title="Horse Facility Dashboard", layout="wide")

st.title("🐴 Horse Facility Profitability Dashboard")

# --- Facility Inputs ---
st.header("📍 Facility Details")
col1, col2 = st.columns(2)
with col1:
    property_value = st.number_input("Total Property Value", step=1000.0)
    property_size = st.number_input("Property Size (hectares)", step=0.1)
    property_tax = st.number_input("Annual Property Taxes", step=100.0)
    insurance = st.number_input("Annual Insurance", step=100.0)
with col2:
    maintenance = st.number_input("Annual Maintenance", step=100.0)
    appreciation = st.number_input("Annual Appreciation (%)", step=0.1)
    depreciation = st.number_input("Annual Depreciation (%)", step=0.1)

# --- Revenue Inputs ---
st.header("💵 Revenue")
basic_boarding = st.number_input("Basic Boarding Price", step=10.0)
horses_boarded = st.number_input("Number of Boarded Horses", step=1)

# --- Cost Inputs ---
st.header("🐎 Per-Horse Monthly Costs")
feed = st.number_input("Feed Cost", step=10.0)
labor = st.number_input("Labor Cost", step=10.0)
utilities = st.number_input("Utilities", step=10.0)
misc = st.number_input("Misc Per-Horse Cost", step=10.0)

# --- Calculations ---
monthly_income = basic_boarding * horses_boarded
monthly_cost = (feed + labor + utilities + misc) * horses_boarded
monthly_profit = monthly_income - monthly_cost
annual_profit = monthly_profit * 12

st.header("📊 Quarterly Results & Year-End Summary")

# --- Current Quarter (Live Calculation) ---
monthly_income = basic_boarding * horses_boarded
monthly_cost = (feed + labor + utilities + misc) * horses_boarded
monthly_profit = monthly_income - monthly_cost
current_quarter = monthly_profit * 3

# --- Display Current Quarter ---
st.subheader("🟢 Current Quarter (Auto-Calculated)")
st.metric("📈 Current Quarter", f"${current_quarter:,.2f}")

# --- Manual Entry: Quarter 1–4 ---
st.subheader("📝 Enter Past/Future Quarter Results")
col1, col2, col3, col4 = st.columns(4)
with col1:
    manual_q1 = st.number_input("Quarter 1", step=100.0)
with col2:
    manual_q2 = st.number_input("Quarter 2", step=100.0)
with col3:
    manual_q3 = st.number_input("Quarter 3", step=100.0)
with col4:
    manual_q4 = st.number_input("Quarter

