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

st.header("📊 Results")
st.metric("Monthly Profit", f"${monthly_profit:,.2f}")
st.metric("Annual Profit", f"${annual_profit:,.2f}")
