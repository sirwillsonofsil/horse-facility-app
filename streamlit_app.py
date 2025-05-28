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

def annual_expense_block(label, key_prefix):
    st.markdown(f"### {label}")
    col1, col2 = st.columns([1.5, 2])
    value = col1.number_input("Annual Value", min_value=0.0, step=100.0, key=f"{key_prefix}_value")
    description = col2.text_input("Description", key=f"{key_prefix}_description")
    quarterly = value / 4
    st.markdown(f"**Quarterly Total:** ${quarterly:,.2f}")
    if description:
        st.markdown(f"📝 _Description: {description}_")
    return quarterly

q_insurance = expense_block("Property Insurance", "insurance")
q_rent = expense_block("Property Rent", "rent")
q_electric = expense_block("General Electric", "electric")
q_water = expense_block("General Water", "water")
q_maintenance = annual_expense_block("Maintenance", "maintenance")
q_misc = annual_expense_block("Miscellaneous", "misc")

total_quarterly_facility_expense = q_insurance + q_rent + q_electric + q_water + q_maintenance + q_misc
st.subheader("🏁 Total Facility Expenses (Quarterly)")
st.metric("Quarterly Total", f"${total_quarterly_facility_expense:,.2f}")

# --- Occupancy Inputs ---
st.header("🏠 Occupancy")
total_stalls = st.number_input("Total Stalls", min_value=0, step=1, key="total_stalls")

col1, col2 = st.columns([1, 1])
fullboard_training = col1.number_input("Fullboard Training", min_value=0, step=1, key="fullboard_training")
fullboard_training_price = col2.number_input("Price (Per Month)", min_value=0.0, step=10.0, key="fullboard_training_price")

col1, col2 = st.columns([1, 1])
half_board = col1.number_input("Half Board", min_value=0, step=1, key="half_board")
half_board_price = col2.number_input("Price (Per Month)", min_value=0.0, step=10.0, key="half_board_price")

col1, col2 = st.columns([1, 1])
company_horses = col1.number_input("Company Horses", min_value=0, step=1, key="company_horses")
company_horses_price = col2.number_input("Price (Per Month)", min_value=0.0, step=10.0, key="company_horses_price")

col1, col2, col3 = st.columns([1, 1, 1])
horse_hotel = col1.number_input("Horse Hotel", min_value=0, step=1, key="horse_hotel")
horse_hotel_price = col2.number_input("Price (Per Night)", min_value=0.0, step=10.0, key="horse_hotel_price")
horse_hotel_nights = col3.number_input("Number of Nights", min_value=0, step=1, key="horse_hotel_nights")

col1, col2 = st.columns([1, 1])
retirement_recovery_horse = col1.number_input("Retirement/Recovery Horse", min_value=0, step=1, key="retirement_recovery_horse")
retirement_recovery_horse_price = col2.number_input("Price (Per Month)", min_value=0.0, step=10.0, key="retirement_recovery_horse_price")

# Occupancy Calculations
total_horses = fullboard_training + half_board + company_horses + retirement_recovery_horse
remaining_stalls = total_stalls - total_horses
monthly_occupancy_revenue = (
    fullboard_training * fullboard_training_price +
    half_board * half_board_price +
    company_horses * company_horses_price +
    horse_hotel * horse_hotel_price * horse_hotel_nights +
    retirement_recovery_horse * retirement_recovery_horse_price
)
quarterly_occupancy_revenue = monthly_occupancy_revenue * 3
annual_occupancy_revenue = monthly_occupancy_revenue * 12

st.subheader("📊 Occupancy Summary")
col1, col2 = st.columns(2)
col1.metric("Total Horses", f"{total_horses}")
col2.metric("Remaining Stalls", f"{remaining_stalls} (-{horse_hotel})")
col1.metric("Quarterly Total Revenue", f"${quarterly_occupancy_revenue:,.2f}")
col2.metric("Annual Total Revenue", f"${annual_occupancy_revenue:,.2f}")

# --- Revenue Inputs ---
st.header("💵 Revenue")
# No inputs here as pricing is now handled in Occupancy section

# --- Cost Inputs ---
st.header("🐎 Per-Horse Monthly Costs")
feed = st.number_input("Feed Cost", min_value=0.0, step=10.0)
labor = st.number_input("Labor Cost", min_value=0.0, step=10.0)
utilities = st.number_input("Utilities", min_value=0.0, step=10.0)
misc = st.number_input("Misc Per-Horse Cost", min_value=0.0, step=10.0)

# --- Calculations ---
monthly_income = monthly_occupancy_revenue
monthly_cost = (feed + labor + utilities + misc) * total_horses
monthly_profit = monthly_income - monthly_cost
current_quarter = monthly_profit * 3
projected_annual = monthly_profit * 12

# --- Quarterly Results & Year-End Summary ---
st.header("📊 Quarterly Results & Year-End Summary")

# --- Projected Quarter and Annual ---
st.subheader("🟢 Projected Results (Auto-Calculated)")
col1, col2 = st.columns(2)
col1.metric("Projected Quarter Profit", f"${current_quarter:,.2f}")
col2.metric("Projected Annual Profit", f"${projected_annual:,.2f}")

# --- Manual Quarterly Inputs ---
st.subheader("📝 Enter Manual Results for Quarters 1–4")
col1, col2, col3, col4 = st.columns(4)
manual_q1 = col1.number_input("Quarter 1 Profit", min_value=0.0, step=100.0)
manual_q2 = col2.number_input("Quarter 2 Profit", min_value=0.0, step=100.0)
manual_q3 = col3.number_input("Quarter 3 Profit", min_value=0.0, step=100.0)
manual_q4 = col4.number_input("Quarter 4 Profit", min_value=0.0, step=100.0)

# --- 4/4 Calculation ---
four_quarter_total = manual_q1 + manual_q2 + manual_q3 + manual_q4
st.subheader("📅 4/4 Calculation")
st.metric("Total of Manual Quarters", f"${four_quarter_total:,.2f}")
