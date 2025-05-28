import streamlit as st

st.set_page_config(page_title="Horse Facility Dashboard", layout="wide")

st.title("🐴 Horse Facility Profitability Dashboard")

# --- Facility Inputs ---
st.header("🏢 Facility Expenses")

# Input mode selector
input_mode = st.selectbox("Input Mode", ["Annual", "Quarterly", "Monthly"], key="facility_input_mode")

def convert_expense(label, key_suffix):
    if input_mode == "Annual":
        annual = st.number_input(f"{label} (Annual)", step=100.0, key=f"annual_{key_suffix}")
        quarterly = annual / 4
        monthly = annual / 12
    elif input_mode == "Quarterly":
        quarterly = st.number_input(f"{label} (Quarterly)", step=100.0, key=f"quarterly_{key_suffix}")
        annual = quarterly * 4
        monthly = annual / 12
    else:  # Monthly
        monthly = st.number_input(f"{label} (Monthly)", step=100.0, key=f"monthly_{key_suffix}")
        annual = monthly * 12
        quarterly = annual / 4

    col1, col2, col3 = st.columns(3)
    col1.metric(f"{label} (Annual)", f"${annual:,.2f}")
    col2.metric(f"{label} (Quarterly)", f"${quarterly:,.2f}")
    col3.metric(f"{label} (Monthly)", f"${monthly:,.2f}")
    return annual

# --- Expense Types ---
insurance_annual = convert_expense("Property Insurance", "insurance")
rent_annual = convert_expense("Property Rent", "rent")
electric_annual = convert_expense("General Electric", "electric")
water_annual = convert_expense("General Water", "water")
maintenance_annual = convert_expense("Maintenance", "maintenance")
misc_annual = convert_expense("Miscellaneous", "misc")

# Total Facility Cost (optional summary)
total_facility_expense_annual = sum([
    insurance_annual,
    rent_annual,
    electric_annual,
    water_annual,
    maintenance_annual,
    misc_annual
])
st.subheader("🏁 Total Facility Expenses")
st.metric("Total Annual Facility Expenses", f"${total_facility_expense_annual:,.2f}")

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
st.metric(label="📈 Current Quarter", value=f"${current_quarter:,.2f}")

# --- Manual Entry for Quarters 1–4 ---
st.subheader("📝 Enter Manual Results for Quarters 1–4")
col1, col2, col3, col4 = st.columns(4)

manual_q1 = col1.number_input("Quarter 1", step=100.0)
manual_q2 = col2.number_input("Quarter 2", step=100.0)
manual_q3 = col3.number_input("Quarter 3", step=100.0)
manual_q4 = col4.number_input("Quarter 4", step=100.0)

# --- Year-End Summary ---
year_end_total = manual_q1 + manual_q2 + manual_q3 + manual_q4

st.subheader("📅 Year-End Summary")
st.metric(label="📊 Total of All Quarters", value=f"${year_end_total:,.2f}")
