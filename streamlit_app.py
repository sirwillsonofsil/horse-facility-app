import streamlit as st

st.set_page_config(page_title="Gelbstein Ranch Profitability Dashboard", layout="wide")
st.title("🌵 Gelbstein Ranch Profitability Dashboard 🌵")

# Initialize revenue variables to prevent NameError
monthly_occupancy_revenue = 0.0
monthly_additional_revenue = 0.0

# --- Property Expenses Inputs ---
st.header("🏠 Property Expenses")

def expense_block(label, key_prefix):
    col1, col2 = st.columns([1, 1.5])
    mode = col1.selectbox("Input Mode", ["Annual", "Quarterly", "Monthly"], key=f"{key_prefix}_mode")
    value = col2.number_input(f"{label}", min_value=0.0, step=100.0, key=f"{key_prefix}_value")
    if mode == "Annual":
        quarterly = value / 4
    elif mode == "Monthly":
        quarterly = value * 3
    else:
        quarterly = value
    return quarterly

q_insurance = expense_block("Insurance", "insurance")
q_rent = expense_block("Rent", "rent")
q_electric = expense_block("Base Electric", "electric")
q_water = expense_block("Base Water", "water")

total_quarterly_property_expense = q_insurance + q_rent + q_electric + q_water
total_annual_property_expense = total_quarterly_property_expense * 4

st.subheader("🏁 Total Property Expenses")
col1, col2 = st.columns(2)
col1.metric("Quarterly Total", f"€{total_quarterly_property_expense:,.2f}")
col2.metric("Annual Total", f"€{total_annual_property_expense:,.2f}")

# --- Occupancy Inputs ---
st.header("🐎 Occupancy")
col1, col2, col3 = st.columns([1, 1, 1])
total_stalls = col1.number_input("Total Stalls", min_value=0, step=1, key="total_stalls")
company_horses = col2.number_input("Company Horses", min_value=0, step=1, key="company_horses")
open_barn_horses = col3.number_input("Open Barn Horses", min_value=0, step=1, key="open_barn_horses")

col1, col2 = st.columns([1, 1])
fullboard_training = col1.number_input("Fullboard Training", min_value=0, step=1, key="fullboard_training")
fullboard_training_price = col2.number_input("Price (Per Month)", min_value=0.0, step=10.0, key="fullboard_training_price")

col1, col2 = st.columns([1, 1])
half_board = col1.number_input("Half Board", min_value=0, step=1, key="half_board")
half_board_price = col2.number_input("Price (Per Month)", min_value=0.0, step=10.0, key="half_board_price")

col1, col2 = st.columns([1, 1])
retirement_recovery_horse = col1.number_input("Retirement/Recovery Horse", min_value=0, step=1, key="retirement_recovery_horse")
retirement_recovery_horse_price = col2.number_input("Price (Per Month)", min_value=0.0, step=10.0, key="retirement_recovery_horse_price")

# Occupancy Calculations
total_horses = fullboard_training + half_board + company_horses + retirement_recovery_horse + open_barn_horses
remaining_stalls = total_stalls - (fullboard_training + half_board + company_horses + retirement_recovery_horse)  # Open Barn Horses do not reduce stalls
monthly_occupancy_revenue = (
    fullboard_training * fullboard_training_price +
    half_board * half_board_price +
    retirement_recovery_horse * retirement_recovery_horse_price
)  # No revenue from Company Horses or Open Barn Horses
quarterly_occupancy_revenue = monthly_occupancy_revenue * 3
annual_occupancy_revenue = monthly_occupancy_revenue * 12

st.subheader("📊 Occupancy Summary")
col1, col2 = st.columns(2)
col1.metric("Total Horses", f"{total_horses}")
col2.metric("Remaining Stalls", f"{remaining_stalls}")
col1.metric("Quarterly Occupancy Revenue", f"€{quarterly_occupancy_revenue:,.2f}")
col2.metric("Annual Occupancy Revenue", f"€{annual_occupancy_revenue:,.2f}")

# --- Company Revenue Inputs ---
st.header("💵 Company Revenue")

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
horse_hotel_count = col1.number_input("Horse Hotel Guest Stays", min_value=0, step=1, key="horse_hotel_count")
horse_hotel_price = col2.number_input("Price (Per Night)", min_value=0.0, step=10.0, key="horse_hotel_price")

col1, col2 = st.columns([1, 1])
led_rides_count = col1.number_input("Led Pony Rides", min_value=0, step=1, key="led_rides_count")
led_rides_price = col2.number_input("Price (Per Half Hour)", min_value=0.0, step=10.0, key="led_rides_price")

# Company Revenue Calculations
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

st.subheader("📊 Total Added Revenue")
col1, col2 = st.columns(2)
col1.metric("Quarterly Total Revenue", f"€{quarterly_additional_revenue:,.2f}")
col2.metric("Annual Total Revenue", f"€{annual_additional_revenue:,.2f}")

# --- Per-Horse Costs ---
st.header("🐎 Per-Horse Costs")

def feed_cost_block():
    st.subheader("Feed")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    bale_type = col1.selectbox("Bale Type", ["Square Bales", "Round Bales"], key="feed_bale_type")
    price_per_bale = col2.number_input("Price Per Bale (€)", min_value=0.0, step=1.0, key="feed_price_per_bale")
    horses_fed_per_month = col3.number_input("Horses Fed Per Month", min_value=1, step=1, key="feed_horses_fed", value=1)  # Default to 1 to avoid division by zero
    
    # Calculate cost per horse
    if horses_fed_per_month > 0:
        monthly_cost_per_horse = price_per_bale / horses_fed_per_month
    else:
        monthly_cost_per_horse = 0.0
    
    daily_cost_per_horse = monthly_cost_per_horse / 30
    yearly_cost_per_horse = monthly_cost_per_horse * 12
    
    # Display totals
    col1, col2, col3 = st.columns([1, 1, 1])
    col1.metric("Daily Cost Per Horse", f"€{daily_cost_per_horse:,.2f}")
    col2.metric("Monthly Cost Per Horse", f"€{monthly_cost_per_horse:,.2f}")
    col3.metric("Yearly Cost Per Horse", f"€{yearly_cost_per_horse:,.2f}")
    
    return monthly_cost_per_horse

def cost_block(label, key_prefix):
    st.subheader(label)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    # Initialize session state
    if f"{key_prefix}_daily" not in st.session_state:
        st.session_state[f"{key_prefix}_daily"] = 0.0
        st.session_state[f"{key_prefix}_monthly"] = 0.0
        st.session_state[f"{key_prefix}_yearly"] = 0.0

    def update_from_daily():
        st.session_state[f"{key_prefix}_monthly"] = st.session_state[f"{key_prefix}_daily"] * 30
        st.session_state[f"{key_prefix}_yearly"] = st.session_state[f"{key_prefix}_daily"] * 365

    def update_from_monthly():
        st.session_state[f"{key_prefix}_daily"] = st.session_state[f"{key_prefix}_monthly"] / 30
        st.session_state[f"{key_prefix}_yearly"] = st.session_state[f"{key_prefix}_monthly"] * 12

    def update_from_yearly():
        st.session_state[f"{key_prefix}_daily"] = st.session_state[f"{key_prefix}_yearly"] / 365
        st.session_state[f"{key_prefix}_monthly"] = st.session_state[f"{key_prefix}_yearly"] / 12

    # Daily input
    daily = col1.number_input("Daily", min_value=0.0, step=0.01, key=f"{key_prefix}_daily", value=st.session_state[f"{key_prefix}_daily"], on_change=update_from_daily)

    # Monthly input
    monthly = col2.number_input("Monthly", min_value=0.0, step=0.01, key=f"{key_prefix}_monthly", value=st.session_state[f"{key_prefix}_monthly"], on_change=update_from_monthly)

    # Yearly input
    yearly = col3.number_input("Yearly", min_value=0.0, step=0.01, key=f"{key_prefix}_yearly", value=st.session_state[f"{key_prefix}_yearly"], on_change=update_from_yearly)

    return st.session_state[f"{key_prefix}_monthly"]

feed_monthly = feed_cost_block()
bedding_monthly = cost_block("Bedding", "bedding")
water_monthly = cost_block("Water", "water")
electricity_monthly = cost_block("Electricity", "electricity")
waste_disposal_monthly = cost_block("Waste Disposal", "waste_disposal")

# Total Per-Horse Cost Summary
total_per_horse_monthly_cost = feed_monthly + bedding_monthly + water_monthly + electricity_monthly + waste_disposal_monthly
total_monthly_cost = total_per_horse_monthly_cost * total_horses
total_quarterly_cost = total_monthly_cost * 3
total_yearly_cost = total_monthly_cost * 12

st.subheader("📊 Total Per-Horse Cost Summary")
col1, col2 = st.columns(2)
col1.metric("Number of Horses", f"{total_horses}")
col2.metric("Total Per-Horse Monthly Cost", f"€{total_per_horse_monthly_cost:,.2f}")
col1.metric("Total Monthly Cost", f"€{total_monthly_cost:,.2f}")
col2.metric("Total Quarterly Cost", f"€{total_quarterly_cost:,.2f}")
col1.metric("Total Yearly Cost", f"€{total_yearly_cost:,.2f}")

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
col1.metric("Quarterly Total", f"€{total_quarterly_company_expense:,.2f}")
col2.metric("Annual Total", f"€{total_annual_company_expense:,.2f}")

# --- Calculations ---
monthly_income = monthly_occupancy_revenue + monthly_additional_revenue
monthly_cost = (
    total_monthly_cost +  # Already includes total_horses multiplication
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
col1.metric("Projected Quarter Profit", f"€{current_quarter:,.2f}")
col2.metric("Projected Annual Profit", f"€{projected_annual:,.2f}")

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
st.metric("Total of Manual Quarters", f"€{four_quarter_total:,.2f}")
