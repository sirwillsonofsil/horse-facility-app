import streamlit as st

st.set_page_config(page_title="Horse Facility Dashboard", layout="wide")

st.title("🐴 Horse Facility Profitability Dashboard")

# --- Facility Inputs ---
st.header("🏢 Facility")

# Flexible input block (Annual, Quarterly, Monthly → all standardized to quarterly)
def expense_block(label, key_prefix):
    st.markdown(f"### {label}")
    col1, col2 = st.columns([1, 2])
    mode = col1.selectbox("Input Mode", ["Annual", "Quarterly", "Monthly"], key=f"{key_prefix}_mode")
    value = col2.number_input("Value", step=100.0, key=f"{key_prefix}_value")

    if mode == "Annual":
        quarterly = value / 4
    elif mode == "Monthly":
        quarterly = value * 3
    else:
        quarterly = value

    st.markdown(f"**Quarterly Total:** ${quarterly:,.2f}")
    return quarterly

# Annual-only input with optional comment
def annual_only_block(label, key_prefix):
    st.markdown(f"### {label}")
    col1, col2 = st.columns([1.5, 2])
    value = col1.number_input("Annual Value", step=100.0, key=f"{key_prefix}_value")
    note = col2.text_input("Comment (optional)", key=f"{key_prefix}_note")
    quarterly = value / 4
    st.markdown(f"**Quarterly Total:** ${quarterly:,.2f}")
    if note:
        st.markdown(f"📝 _Note: {note}_")
    return quarterly

# --- Expense Entries ---
q_insurance = expense_block("Property Insurance", "insurance")
q_rent = expense_block("Property Rent", "rent")
q_electric = expense_block("General Electric", "electric")
q_water = expense_block("General Water", "water")

q_maintenance = annual_only_block("Maintenance", "maintenance")
q_misc = annual_only_block("Miscellaneous", "misc")

# --- Quarterly Total Summary ---
total_quarterly_facility_expense = (
    q_insurance + q_rent + q_electric + q_water + q_maintenance + q_misc
)

st.subheader("🏁 Total Facility Expenses (Quarterly)")
st.metric("Quarterly Total", f"${total_quarterly_facility_expense:,.2f}")


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
