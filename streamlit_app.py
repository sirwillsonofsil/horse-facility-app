import streamlit as st

st.set_page_config(page_title="Gelbstein Ranch Profitability Dashboard", layout="wide")
st.title("🌵 Gelbstein Ranch Profitability Dashboard 🌵")

# --- Property Inputs ---
st.header("🏠 Property")  # Using 🏠 with red styling in UI for red barn

def expense_block(label, key_prefix):
    col1, col2 = st.columns([1.5, 1])
    value = col1.number_input(f"{label}", min_value=0.0, step=100.0, key=f"{key_prefix}_value")
    mode = col2.selectbox("Input Mode", ["Annual", "Quarterly", "Monthly"], key=f"{key_prefix}_mode")
    if mode == "Annual":
        quarterly = value / 4
    elif mode == "Monthly":
        quarterly = value * 3
    else:
        quarterly = value
    return quarterly

q_insurance = expense_block("Property Insurance", "insurance")
q_rent = expense_block("Property Rent", "rent")
q_electric = expense_block("General Electric", "electric")
q_water = expense_block("General Water", "water")

total_quarterly_property_expense = q_insurance + q_rent + q_electric + q_water
total_annual_property_expense = total_quarterly_property_expense * 4

st.subheader("🏁 Total Property Expenses")
col1, col2 = st.columns(2)
col1.metric("Quarterly Total", f"${total_quarterly_property_expense:,.2f}")
col2.metric("Annual Total", f"${total_annual_property_expense:,.2f}")

# --- Occupancy Inputs ---
st.header("🐎 Occupancy")
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
    retirement_recovery_horse * retirement_recovery_horse_price
)
quarterly_occupancy_revenue = monthly_occupancy_revenue * 3
annual_occupancy_revenue = monthly_occupancy_revenue * 12

st.subheader("📊 Occupancy Summary")
col1, col2 = st.columns(2)
col1.metric("Total Horses", f"{total_horses}")
col2.metric("Remaining Stalls", f"{remaining_stalls}")
col1.metric("Quarterly Total Revenue", f"${quarterly_occupancy_revenue:,.2f}")
col2.metric("Annual Total Revenue", f"${annual_occupancy_revenue:,.2f}")

# --- Revenue Inputs ---
st.header("💵 Revenue")

col1, col2 = st.columns([1, 1])
ivanka_private_count = col1.number_input("Ivanka Private Lessons", min_value=0, step=1, key="ivanka_private_count")
ivanka_private_price = col2.number_input("Price (Per Session)", min_value=0.0, step=10.0, key="ivanka_private_price")

col1, col2 = st.columns([1, 1])
ivanka_group_count = col1.number_input("Ivanka Group Lessons", min_value=0, step=1, key="ivanka_group_count")
ivanka_group_price = col2.number_input("Price (Per Session)", min_value=0.0, step=10.0, key="ivanka_group_price")

col1, col2 = st.columns([1, 1])
kerry_mobile_count = col1.number_input("Kerry Mobile Sessions", min_value=0, step=1, key="kerry_mobile_count")
kerry_mobile_price = col2.number_input("Price (Per Session)", min_value=0.0, step=10.0, key="kerry_mobile_price")

col1, col2 = st.columns([1, 1])
parkour_guests_count = col1.number_input("Parkour Guests", min_value=0, step=1, key="parkour_guests_count")
parkour_guests_price = col2.number_input("Price (Per Guest)", min_value=0.0, step=10.0, key="parkour_guests_price")

col1, col2 = st.columns([1, 1])
horse_hotel_count = col1.number_input("Horse Hotel Guests", min_value=0, step=1, key="horse_hotel_count")
horse_hotel_price = col2.number_input("Price (Per Night)", min_value=0.0, step=10.0, key="horse_hotel_price")

col1, col2 = st.columns([1, 1])
led_rides_count = col1.number_input("Led Rides", min_value=0, step=1, key="led_rides_count")
led_rides_price = col2.number_input("Price (Per Ride)", min_value=0.0, step=10.0, key="led_rides_price")

# Revenue Calculations
monthly_additional_revenue = (
    ivanka_private_count * ivanka_private_price +
    ivanka_group_count * ivanka_group_price +
    kerry_mobile_count * kerry_mobile_price +
    parkour_guests_count * parkour_guests_price +
    horse_hotel_count * horse_hotel_price +
    led_rides_count * led_rides_price
)
quarterly_additional_revenue = monthly_additional_revenue * 3
annual_additional_revenue = monthly_additional_revenue * 12

st.subheader("📊 Revenue Summary")
col1, col2 = st.columns(2)
col1.metric("Quarterly Total Revenue", f"${quarterly_additional_revenue:,.2f}")
col2.metric("Annual Total Revenue", f"${annual_additional_revenue:,.2f}")

# --- Cost Inputs ---
st.header("🐎 Per-Horse Monthly Costs")

def cost_block(label, key_prefix):
    st.subheader(label)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    # Initialize session state if not present
    if f"{key_prefix}_daily" not in st.session_state:
        st.session_state[f"{key_prefix}_daily"] = 0.0
        st.session_state[f"{key_prefix}_monthly"] = 0.0
        st.session_state[f"{key_prefix}_annual"] = 0.0
        st.session_state[f"{key_prefix}_last_modified"] = None

    def update_values(source, value):
        if source == "daily":
            st.session_state[f"{key_prefix}_monthly"] = value * 30
            st.session_state[f"{key_prefix}_annual"] = value * 365
        elif source == "monthly":
            st.session_state[f"{key_prefix}_daily"] = value / 30
            st.session_state[f"{key_prefix}_annual"] = value * 12
        elif source == "annual":
            st.session_state[f"{key_prefix}_daily"] = value / 365
            st.session_state[f"{key_prefix}_monthly"] = value / 12
        st.session_state[f"{key_prefix}_last_modified"] = source

    # Daily input
    daily = col1.number_input("Daily", min_value=0.0, step=0.01, key=f"{key_prefix}_daily_input", value=st.session_state[f"{key_prefix}_daily"])
    if st.session_state[f"{key_prefix}_last_modified"] != "daily":
        update_values("daily", daily)
        st.session_state[f"{key_prefix}_daily"] = daily

    # Monthly input
    monthly = col2.number_input("Monthly", min_value=0.0, step=0.01, key=f"{key_prefix}_monthly_input", value=st.session_state[f"{key_prefix}_monthly"])
    if st.session_state[f"{key_prefix}_last_modified"] != "monthly":
        update_values("monthly", monthly)
        st.session_state[f"{key_prefix}_monthly"] = monthly

    # Annual input
    annual = col3.number_input("Annual", min_value=0.0, step=0.01, key=f"{key_prefix}_annual_input", value=st.session_state[f"{key_prefix}_annual"])
    if st.session_state[f"{key_prefix}_last_modified"] != "annual":
        update_values("annual", annual)
        st.session_state[f"{key_prefix}_annual"] = annual

    return st.session_state[f"{key_prefix}_monthly"]

feed_monthly = cost_block("Feed Cost", "feed")
labor_monthly = cost_block("Labor Cost", "labor")
utilities_monthly = cost_block("Utilities", "utilities")
misc_monthly = cost_block("Misc Per-Horse Cost", "misc")

# --- Company Expenses ---
st.header("💰 Company Expenses")

def annual_expense_block(label, key_prefix):
    col1, col2 = st.columns([1.5, 2])
    value = col1.number_input(f"{label}", min_value=0.0, step=100.0, key=f"{key_prefix}_value")
    description = col2.text_input("Description", key=f"{key_prefix}_description")
    quarterly = value / 4
    return quarterly

q_maintenance = annual_expense_block("Maintenance", "maintenance")
q_misc = annual_expense_block("Miscellaneous", "misc")

total_quarterly_company_expense = q_maintenance + q_misc
total_annual_company_expense = total_quarterly_company_expense * 4

st.subheader("🏁 Total Company Expenses")
col1, col2 = st.columns(2)
col1.metric("Quarterly Total", f"${total_quarterly_company_expense:,.2f}")
col2.metric("Annual Total", f"${total_annual_company_expense:,.2f}")

# --- Calculations ---
monthly_income = monthly_occupancy_revenue + monthly_additional_revenue
monthly_cost = (
    (feed_monthly + labor_monthly + utilities_monthly + misc_monthly) * total_horses +
    (total_quarterly_property_expense + total_quarterly_company_expense) / 3
)
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
