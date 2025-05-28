import streamlit as st

st.set_page_config(page_title="Horse Facility Dashboard", layout="wide")

st.title("🐴 Horse Facility Profitability Dashboard")

# --- Facility Inputs ---
st.header("🏢 Facility")

# Standard input block for expenses with selectable input mode
def expense_block(label, key_prefix):
    st.subheader(label)

    col1, col2 = st.columns([1, 2])
    mode = col1.selectbox("Input Mode", ["Annual", "Quarterly", "Monthly"], key=f"{key_prefix}_mode")
    value = col2.number_input("Value", step=100.0, key=f"{key_prefix}_value")


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
