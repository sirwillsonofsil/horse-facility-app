import streamlit as st

st.set_page_config(page_title="Horse Facility Dashboard", layout="wide")
st.title("🐴 Horse Facility Profitability Dashboard")

# --- Facility Inputs ---
st.header("🏢 Facility")

def expense_block(label, key_prefix):
    st.markdown(f"### {label}")
    col1, col2 = st.columns([1, 2])
    mode = col1.selectbox("Input Mode", ["Annual", "Quarterly", "Monthly"], key=f"{key_prefix}_mode")
    value = col2.number_input("Value", min_value=0.0, step=100.0, key=f"{key_prefix}_value")
    if mode == "Annual":
        quarterly = value / 4
    elif mode == "Monthly":
        quarterly = value * 3
    else:
        quarterly = value
    st.markdown(f"**Quarterly Total:** ${quarterly:,.2f}")
    return quarterly

def annual_only_block(label, key_prefix):
    st.markdown(f"### {label}")
    col1, col2 = st.columns([1.5, 2])
    value = col1.number_input("Annual Value", min_value=0.0, step=100.0, key=f"{key_prefix}_value")
    note = col2.text_input("Comment (optional)", key=f"{key_prefix}_note")
    quarterly = value / 4
    st.markdown(f"**Quarterly Total:** ${quarterly:,.2f}")
    if note:
        st.markdown(f"📝 _Note: {note}_")
    return quarterly

q_insurance = expense_block("Property Insurance", "insurance")
q_rent = expense_block("Property Rent", "rent")
q_electric = expense_block("General Electric", "electric")
q_water = expense_block("General Water", "water")
q_maintenance = annual_only_block("Maintenance", "maintenance")
q_misc = annual_only_block("Miscellaneous", "misc")

total_quarterly_facility_expense = q_insurance + q_rent + q_electric + q_water + q_maintenance + q_misc
st.subheader("🏁 Total Facility Expenses (Quarterly)")
st.metric("Quarterly Total", f"${total_quarterly_facility_expense:,.2f}")

# --- Revenue Inputs ---
st.header("💵 Revenue")
basic_boarding = st.number_input("Basic Boarding Price", min_value=0.0, step=10.0)
horses_boarded = st.number_input("Number of Boarded Horses", min_value=0, step=1)

# --- Cost Inputs ---
st.header("🐎 Per-Horse Monthly Costs")
feed = st.number_input("Feed Cost", min_value=0.0, step=10.0)
labor = st.number_input("Labor Cost", min_value=0.0, step=10.0)
utilities = st.number_input("Utilities", min_value=0.0, step=10.0)
misc = st.number_input("Misc Per-Horse Cost", min_value=0.0, step=10.0)

# --- Calculations ---
monthly_income = basic_boarding * horses_boarded
monthly_cost = (feed + labor + utilities + misc) * horses_boarded
monthly_profit = monthly_income - monthly_cost
current_quarter = monthly_profit * 3
annual_profit = monthly_profit * 12

# --- Quarterly Results & Year-End Summary ---
st.header("📊 Quarterly Results & Year-End Summary")

# --- Current Quarter ---
st.subheader("🟢 Projected Quarter (Auto-Calculated)")
st.metric("Projected Quarter Profit", f"${current_quarter:,.2f}")

# --- Manual Quarterly Inputs ---
st.subheader("📝 Enter Manual Results for Quarters 1–4")
col1, col2, col3, col4 = st.columns(4)
manual_q1 = col1.number_input("Quarter 1 Profit", min_value=0.0, step=100.0)
manual_q2 = col2.number_input("Quarter 2 Profit", min_value=0.0, step=100.0)
manual_q3 = col3.number_input("Quarter 3 Profit", min_value=0.0, step=100.0)
manual_q4 = col4.number_input("Quarter 4 Profit", min_value=0.0, step=100.0)

# --- Year-End Summary ---
year_end_profit = manual_q1 + manual_q2 + manual_q3 + manual_q4
annual_facility_expenses = total_quarterly_facility_expense * 4
year_end_net_profit = year_end_profit - annual_facility_expenses

st.subheader("📅 Year-End Summary")
st.metric("Total Revenue (Annual)", f"${monthly_income * 12:,.2f}")
st.metric("Total Per-Horse Costs (Annual)", f"${monthly_cost * 12:,.2f}")
st.metric("Total Facility Expenses (Annual)", f"${annual_facility_expenses:,.2f}")
st.metric("Total Profit (All Quarters, After Facility Expenses)", f"${year_end_net_profit:,.2f}")
