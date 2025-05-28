import streamlit as st

# Configure page with title and wide layout
st.set_page_config(page_title="Gelbstein Ranch Profitability Dashboard", layout="wide")
st.title("🌵 Gelbstein Ranch Profitability Dashboard 🌵")

# Initialize revenue variables to avoid errors
monthly_occupancy_revenue = 0.0  # Horse boarding revenue
monthly_additional_revenue = 0.0  # Additional services revenue

# --- Property Expenses ---
st.header("🏠 Property Expenses")

def expense_block(label, key_prefix):
    """Calculate quarterly expense from user input (Annual, Quarterly, Monthly)."""
    col1, col2 = st.columns([1, 1.5])
    mode = col1.selectbox("Input Mode", ["Annual", "Quarterly", "Monthly"], key=f"{key_prefix}_mode")
    value = col2.number_input(f"{label}", min_value=0.0, step=100.0, key=f"{key_prefix}_value")
    if mode == "Annual":
        return value / 4  # Convert to quarterly
    elif mode == "Monthly":
        return value * 3  # Convert to quarterly
    return value  # Quarterly input

# Collect property expenses
q_insurance = expense_block("Insurance", "insurance")
q_rent = expense_block("Rent", "rent")
q_electric = expense_block("Base Electric", "electric")
q_water = expense_block("Base Water", "water")

# Calculate total property expenses
total_quarterly_property_expense = q_insurance + q_rent + q_electric + q_water
total_monthly_property_expense = total_quarterly_property_expense / 3
total_annual_property_expense = total_quarterly_property_expense * 4

# Display property expenses summary
st.subheader("🏁 Total Property Expenses")
col1, col2, col3 = st.columns(3)
col1.metric("Monthly Total", f"€{total_monthly_property_expense:,.2f}")
col2.metric("Quarterly Total", f"€{total_quarterly_property_expense:,.2f}")
col3.metric("Annual Total", f"€{total_annual_property_expense:,.2f}")

# --- Occupancy ---
st.header("🐎 Occupancy")

# Input total stalls and company horses
col1, col2 = st.columns(2)
total_stalls = col1.number_input("Total Stalls", min_value=0, step=1, key="total_stalls")
company_horses = col2.number_input("Company Horses", min_value=0, step=1, key="company_horses")

# Input paying horse categories and prices
col1, col2 = st.columns(2)
open_barn_horses = col1.number_input("Open Barn Horses", min_value=0, step=1, key="open_barn_horses")
open_barn_horses_price = col2.number_input("Price (Per Month)", min_value=0.0, step=10.0, key="open_barn_horses_price")

col1, col2 = st.columns(2)
fullboard_training = col1.number_input("Fullboard Training", min_value=0, step=1, key="fullboard_training")
fullboard_training_price = col2.number_input("Price (Per Month)", min_value=0.0, step=10.0, key="fullboard_training_price")

col1, col2 = st.columns(2)
half_board = col1.number_input("Half Board", min_value=0, step=1, key="half_board")
half_board_price = col2.number_input("Price (Per Month)", min_value=0.0, step=10.0, key="half_board_price")

col1, col2 = st.columns(2)
retirement_recovery_horse = col1.number_input("Retirement/Recovery Horse", min_value=0, step=1, key="retirement_recovery_horse")
retirement_recovery_horse_price = col2.number_input("Price (Per Month)", min_value=0.0, step=10.0, key="retirement_recovery_horse_price")

# Calculate occupancy metrics
total_horses = fullboard_training + half_board + company_horses + retirement_recovery_horse + open_barn_horses
remaining_stalls = total_stalls - (fullboard_training + half_board + company_horses + retirement_recovery_horse)
monthly_occupancy_revenue = (
    fullboard_training * fullboard_training_price +
    half_board * half_board_price +
    retirement_recovery_horse * retirement_recovery_horse_price +
    open_barn_horses * open_barn_horses_price
)
quarterly_occupancy_revenue = monthly_occupancy_revenue * 3
annual_occupancy_revenue = monthly_occupancy_revenue * 12

# Display occupancy summary
st.subheader("📊 Occupancy Summary")
col1, col2 = st.columns(2)
col1.metric("Total Horses", f"{total_horses}")
col2.metric("Remaining Stalls", f"{remaining_stalls}")
col1, col2, col3 = st.columns(3)
col1.metric("Monthly Occupancy Revenue", f"€{monthly_occupancy_revenue:,.2f}")
col2.metric("Quarterly Occupancy Revenue", f"€{quarterly_occupancy_revenue:,.2f}")
col3.metric("Annual Occupancy Revenue", f"€{annual_occupancy_revenue:,.2f}")

# --- Company Revenue ---
st.header("💵 Company Revenue")

# Input service counts and prices
col1, col2 = st.columns(2)
ivanka_private_count = col1.number_input("Ivanka Private Lessons", min_value=0, step=1, key="ivanka_private_count")
ivanka_private_price = col2.number_input("Price (Per Session)", min_value=0.0, step=10.0, key="ivanka_private_price")

col1, col2 = st.columns(2)
ivanka_group_count = col1.number_input("Ivanka Group Lessons", min_value=0, step=1, key="ivanka_group_count")
ivanka_group_price = col2.number_input("Price (Per Session)", min_value=0.0, step=10.0, key="ivanka_group_price")

col1, col2 = st.columns(2)
kerry_mobile_count = col1.number_input("Kerry Mobile Sessions", min_value=0, step=1, key="kerry_mobile_count")
kerry_mobile_price = col2.number_input("Price (Per Session)", min_value=0.0, step=10.0, key="kerry_mobile_price")

col1, col2 = st.columns(2)
parkour_guests_count = col1.number_input("Parkour Guests", min_value=0, step=1, key="parkour_guests_count")
parkour_guests_price = col2.number_input("Price (Per Guest)", min_value=0.0, step=10.0, key="parkour_guests_price")

col1, col2 = st.columns(2)
horse_hotel_count = col1.number_input("Horse Hotel Guest Stays", min_value=0, step=1, key="horse_hotel_count")
horse_hotel_price = col2.number_input("Price (Per Night)", min_value=0.0, step=10.0, key="horse_hotel_price")

col1, col2 = st.columns(2)
led_rides_count = col1.number_input("Led Pony Rides", min_value=0, step=1, key="led_rides_count")
led_rides_price = col2.number_input("Price (Per Half Hour)", min_value=0.0, step=10.0, key="led_rides_price")

# Calculate additional revenue
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

# Display company revenue summary
st.subheader("📊 Total Added Revenue")
col1, col2, col3 = st.columns(3)
col1.metric("Monthly Total Revenue", f"€{monthly_additional_revenue:,.2f}")
col2.metric("Quarterly Total Revenue", f"€{quarterly_additional_revenue:,.2f}")
col3.metric("Annual Total Revenue", f"€{annual_additional_revenue:,.2f}")

# --- Per-Horse Costs ---
st.header("🐎 Per-Horse Costs")

def feed_cost_block():
    """Calculate monthly feed cost per horse based on bale type and price."""
    st.subheader("Feed")
    col1, col2, col3 = st.columns(3)
    bale_type = col1.selectbox("Bale Type", ["Square Bales", "Round Bales"], key="feed_bale_type")
    price_per_bale = col2.number_input("Price Per Bale (€)", min_value=0.0, step=1.0, key="feed_price_per_bale")
    horses_fed_per_month = col3.number_input("Horses Fed Per Month", min_value=1, step=1, key="feed_horses_fed", value=1)
    
    monthly_cost_per_horse = price_per_bale / horses_fed_per_month if horses_fed_per_month > 0 else 0.0
    daily_cost_per_horse = monthly_cost_per_horse / 30
    yearly_cost_per_horse = monthly_cost_per_horse * 12
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Daily Cost Per Horse", f"€{daily_cost_per_horse:,.2f}")
    col2.metric("Monthly Cost Per Horse", f"€{monthly_cost_per_horse:,.2f}")
    col3.metric("Yearly Cost Per Horse", f"€{yearly_cost_per_horse:,.2f}")
    
    return monthly_cost_per_horse

def cost_block(label, key_prefix):
    """Calculate monthly cost per horse with synced daily, monthly, yearly inputs."""
    st.subheader(label)
    col1, col2, col3 = st.columns(3)
    
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

    col1.number_input("Daily", min_value=0.0, step=0.01, key=f"{key_prefix}_daily", value=st.session_state[f"{key_prefix}_daily"], on_change=update_from_daily)
    col2.number_input("Monthly", min_value=0.0, step=0.01, key=f"{key_prefix}_monthly", value=st.session_state[f"{key_prefix}_monthly"], on_change=update_from_monthly)
    col3.number_input("Yearly", min_value=0.0, step=0.01, key=f"{key_prefix}_yearly", value=st.session_state[f"{key_prefix}_yearly"], on_change=update_from_yearly)

    return st.session_state[f"{key_prefix}_monthly"]

# Collect per-horse costs
feed_monthly = feed_cost_block()
bedding_monthly = cost_block("Bedding", "bedding")
water_monthly = cost_block("Water", "water")
electricity_monthly = cost_block("Electricity", "electricity")
waste_disposal_monthly = cost_block("Waste Disposal", "waste_disposal")

# Calculate total per-horse costs
total_per_horse_monthly_cost = feed_monthly + bedding_monthly + water_monthly + electricity_monthly + waste_disposal_monthly
total_monthly_cost = total_per_horse_monthly_cost * total_horses
total_quarterly_cost = total_monthly_cost * 3
total_yearly_cost = total_monthly_cost * 12

# Display per-horse cost summary
st.subheader("📊 Total Per-Horse Cost Summary")
col1, col2 = st.columns(2)
col1.metric("Number of Horses", f"{total_horses}")
col2.metric("Total Per-Horse Monthly Cost", f"€{total_per_horse_monthly_cost:,.2f}")
col1, col2, col3 = st.columns(3)
col1.metric("Total Monthly Cost", f"€{total_monthly_cost:,.2f}")
col2.metric("Total Quarterly Cost", f"€{total_quarterly_cost:,.2f}")
col3.metric("Total Yearly Cost", f"€{total_yearly_cost:,.2f}")

# --- Company Expenses ---
st.header("💰 Company Expenses")

def annual_expense_block(label, key_prefix):
    """Calculate quarterly expense from annual input with description."""
    col1, col2 = st.columns([1.5, 2])
    value = col1.number_input(f"{label}", min_value=0.0, step=100.0, key=f"{key_prefix}_value")
    col2.text_input("Description", key=f"{key_prefix}_description")
    return value / 4  # Convert to quarterly

# Collect company expenses
q_maintenance = annual_expense_block("Maintenance", "maintenance")
q_misc = annual_expense_block("Miscellaneous", "misc")

# Calculate total company expenses
total_quarterly_company_expense = q_maintenance + q_misc
total_monthly_company_expense = total_quarterly_company_expense / 3
total_annual_company_expense = total_quarterly_company_expense * 4

# Display company expenses summary
st.subheader("🏁 Total Company Expenses")
col1, col2, col3 = st.columns(3)
col1.metric("Monthly Total", f"€{total_monthly_company_expense:,.2f}")
col2.metric("Quarterly Total", f"€{total_quarterly_company_expense:,.2f}")
col3.metric("Annual Total", f"€{total_annual_company_expense:,.2f}")

# --- Financial Calculations ---
monthly_income = monthly_occupancy_revenue + monthly_additional_revenue
monthly_cost = total_monthly_cost + (total_quarterly_property_expense + total_quarterly_company_expense) / 3
monthly_profit = monthly_income - monthly_cost
current_quarter = monthly_profit * 3
projected_annual = monthly_profit * 12

# --- Quarterly Results & Year-End Summary ---
st.header("📊 Quarterly Results & Year-End Summary")

# Display projected profits
st.subheader("🟢 Projected Results")
col1, col2 = st.columns(2)
col1.metric("Projected Quarter Profit", f"€{current_quarter:,.2f}")
col2.metric("Projected Annual Profit", f"€{projected_annual:,.2f}")

# Input manual quarterly profits
st.subheader("📝 Manual Quarterly Profits")
col1, col2, col3, col4 = st.columns(4)
manual_q1 = col1.number_input("Quarter 1 Profit", min_value=0.0, step=100.0)
manual_q2 = col2.number_input("Quarter 2 Profit", min_value=0.0, step=100.0)
manual_q3 = col3.number_input("Quarter 3 Profit", min_value=0.0, step=100.0)
manual_q4 = col4.number_input("Quarter 4 Profit", min_value=0.0, step=100.0)

# Calculate and display total manual profits
four_quarter_total = manual_q1 + manual_q2 + manual_q3 + manual_q4
st.subheader("📅 Annual Total")
st.metric("Total of Manual Quarters", f"€{four_quarter_total:,.2f}")
