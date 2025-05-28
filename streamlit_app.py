import streamlit as st

# Time conversion constants for consistent calculations
DAYS_PER_MONTH = 30  # 30 days/month simplifies monthly cost estimates
DAYS_PER_YEAR = 365  # 365 days/year aligns with standard annual projections

# Configure page layout and title with ranch theme
st.set_page_config(page_title="Gelbstein Ranch Profitability Dashboard", layout="wide")
st.title("🌵 Gelbstein Ranch Profitability Dashboard 🌵")

# Initialize revenue variables to avoid undefined errors
monthly_occupancy_revenue = 0.0  # Tracks horse boarding income
monthly_additional_revenue = 0.0  # Tracks service-based income

# --- Property Expenses ---
st.header("🏠 Property Expenses")  # Fixed costs for ranch property

# Handles expense inputs with flexible time modes
# - label: Expense name (e.g., "Insurance")
# - key_prefix: Unique key for inputs
# - is_annual: Forces annual input if True
# - include_description: Adds description field if True
# Returns quarterly expense for unified calculations
def expense_block(label, key_prefix, is_annual=False, include_description=False):
    col1, col2 = st.columns([1, 1.5])  # Layout: mode/value + optional description
    if is_annual:
        value = col1.number_input(f"{label} (Annual)", min_value=0.0, step=100.0, key=f"{key_prefix}_value")
        quarterly = value / 4  # Annual to quarterly for consistency
    else:
        mode = col1.selectbox("Input Mode", ["Annual", "Quarterly", "Monthly"], key=f"{key_prefix}_mode")
        value = col2.number_input(f"{label}", min_value=0.0, step=100.0, key=f"{key_prefix}_value")
        quarterly = value / 4 if mode == "Annual" else value * 3 if mode == "Monthly" else value
    if include_description:
        col2.text_input("Description", key=f"{key_prefix}_description")  # Optional context for expense
    return quarterly

# Property expense inputs
quarterly_insurance_expense = expense_block("Insurance", "insurance")  # Covers property insurance
quarterly_rent_expense = expense_block("Rent", "rent")  # Base rent cost
quarterly_electric_expense = expense_block("Base Electric", "electric")  # Fixed electric cost
quarterly_water_expense = expense_block("Base Water", "water")  # Fixed water cost

# Total property expenses across time periods
total_quarterly_property_expense = sum([quarterly_insurance_expense, quarterly_rent_expense, quarterly_electric_expense, quarterly_water_expense])
total_monthly_property_expense = total_quarterly_property_expense / 3  # Quarterly to monthly
total_annual_property_expense = total_quarterly_property_expense * 4  # Quarterly to annual

# Display totals in one row for clarity
st.subheader("🏁 Total Property Expenses")
col1, col2, col3 = st.columns([1, 1, 1])
col1.metric("Monthly Total", f"€{total_monthly_property_expense:,.2f}")
col2.metric("Quarterly Total", f"€{total_quarterly_property_expense:,.2f}")
col3.metric("Annual Total", f"€{total_annual_property_expense:,.2f}")

# --- Occupancy ---
st.header("🐎 Occupancy")  # Horse boarding and stall usage

# Total stalls and company horses on one row
col1, col2 = st.columns([1.5, 1.5])
total_stalls = col1.number_input("Total Stalls", min_value=0, step=1, key="total_stalls")  # Fixed stall capacity
company_horses = col2.number_input("Company Horses", min_value=0, step=1, key="company_horses")  # Non-paying horses

# Paying horse categories with prices
col1, col2 = st.columns([1, 1])
open_barn_horses = col1.number_input("Open Barn Horses", min_value=0, step=1, key="open_barn_horses")  # No stall usage
open_barn_horses_price = col2.number_input("Price (Per Month)", min_value=0.0, step=10.0, key="open_barn_horses_price")

col1, col2 = st.columns([1, 1])
fullboard_training = col1.number_input("Fullboard Training", min_value=0, step=1, key="fullboard_training")  # Full-service boarding
fullboard_training_price = col2.number_input("Price (Per Month)", min_value=0.0, step=10.0, key="fullboard_training_price")

col1, col2 = st.columns([1, 1])
half_board = col1.number_input("Half Board", min_value=0, step=1, key="half_board")  # Partial boarding
half_board_price = col2.number_input("Price (Per Month)", min_value=0.0, step=10.0, key="half_board_price")

col1, col2 = st.columns([1, 1])
retirement_recovery_horse = col1.number_input("Retirement/Recovery Horse", min_value=0, step=1, key="retirement_recovery_horse")  # Special care horses
retirement_recovery_horse_price = col2.number_input("Price (Per Month)", min_value=0.0, step=10.0, key="retirement_recovery_horse_price")

# Occupancy calculations
total_horses = sum([fullboard_training, half_board, company_horses, retirement_recovery_horse, open_barn_horses])  # All horses tracked
remaining_stalls = total_stalls - (fullboard_training + half_board + company_horses + retirement_recovery_horse)  # Open barn horses don’t use stalls
monthly_occupancy_revenue = sum([
    fullboard_training * fullboard_training_price,
    half_board * half_board_price,
    retirement_recovery_horse * retirement_recovery_horse_price,
    open_barn_horses * open_barn_horses_price
])  # Revenue from paying horses only
quarterly_occupancy_revenue = monthly_occupancy_revenue * 3
annual_occupancy_revenue = monthly_occupancy_revenue * 12

# Occupancy summary
st.subheader("📊 Occupancy Summary")
col1, col2 = st.columns(2)
col1.metric("Total Horses", f"{total_horses}")
col2.metric("Remaining Stalls", f"{remaining_stalls}")
col1, col2, col3 = st.columns([1, 1, 1])
col1.metric("Monthly Occupancy Revenue", f"€{monthly_occupancy_revenue:,.2f}")
col2.metric("Quarterly Occupancy Revenue", f"€{quarterly_occupancy_revenue:,.2f}")
col3.metric("Annual Occupancy Revenue", f"€{annual_occupancy_revenue:,.2f}")

# --- Company Revenue ---
st.header("💵 Company Revenue")  # Additional service income

# Service inputs (assumed monthly)
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

# Revenue calculations
monthly_additional_revenue = sum([
    ivanka_private_count * ivanka_private_price,
    ivanka_group_count * ivanka_group_price,
    kerry_mobile_count * kerry_mobile_price,
    parkour_guests_count * parkour_guests_price,
    horse_hotel_count * horse_hotel_price,
    led_rides_count * led_rides_price
])  # Assumes monthly counts
quarterly_additional_revenue = monthly_additional_revenue * 3
annual_additional_revenue = monthly_additional_revenue * 12

# Revenue summary
st.subheader("📊 Total Added Revenue")
col1, col2, col3 = st.columns([1, 1, 1])
col1.metric("Monthly Total Revenue", f"€{monthly_additional_revenue:,.2f}")
col2.metric("Quarterly Total Revenue", f"€{quarterly_additional_revenue:,.2f}")
col3.metric("Annual Total Revenue", f"€{annual_additional_revenue:,.2f}")

# --- Per-Horse Costs ---
st.header("🐎 Per-Horse Costs")  # Variable costs per horse

# Calculates feed cost per horse
def feed_cost_block():
    st.subheader("Feed")
    col1, col2, col3 = st.columns([1, 1, 1])
    bale_type = col1.selectbox("Bale Type", ["Square Bales", "Round Bales"], key="feed_bale_type")  # Placeholder for future cost adjustments
    price_per_bale = col2.number_input("Price Per Bale (€)", min_value=0.0, step=1.0, key="feed_price_per_bale")
    horses_fed_per_month = col3.number_input("Horses Fed Per Month", min_value=1, step=1, key="feed_horses_fed", value=1)  # Min 1 avoids division error
    monthly_cost_per_horse = price_per_bale / horses_fed_per_month if horses_fed_per_month > 0 else 0.0  # Cost split among horses
    daily_cost_per_horse = monthly_cost_per_horse / DAYS_PER_MONTH
    yearly_cost_per_horse = monthly_cost_per_horse * 12
    col1, col2, col3 = st.columns([1, 1, 1])
    col1.metric("Daily Cost Per Horse", f"€{daily_cost_per_horse:,.2f}")
    col2.metric("Monthly Cost Per Horse", f"€{monthly_cost_per_horse:,.2f}")
    col3.metric("Yearly Cost Per Horse", f"€{yearly_cost_per_horse:,.2f}")
    return monthly_cost_per_horse

# Handles other per-horse costs with synced inputs
def cost_block(label, key_prefix):
    st.subheader(label)
    col1, col2, col3 = st.columns([1, 1, 1])
    if f"{key_prefix}_daily" not in st.session_state:
        st.session_state[f"{key_prefix}_daily"] = 0.0  # Initialize defaults
        st.session_state[f"{key_prefix}_monthly"] = 0.0
        st.session_state[f"{key_prefix}_yearly"] = 0.0
    def update_from_daily():
        st.session_state[f"{key_prefix}_monthly"] = st.session_state[f"{key_prefix}_daily"] * DAYS_PER_MONTH
        st.session_state[f"{key_prefix}_yearly"] = st.session_state[f"{key_prefix}_daily"] * DAYS_PER_YEAR
    def update_from_monthly():
        st.session_state[f"{key_prefix}_daily"] = st.session_state[f"{key_prefix}_monthly"] / DAYS_PER_MONTH
        st.session_state[f"{key_prefix}_yearly"] = st.session_state[f"{key_prefix}_monthly"] * 12
    def update_from_yearly():
        st.session_state[f"{key_prefix}_daily"] = st.session_state[f"{key_prefix}_yearly"] / DAYS_PER_YEAR
        st.session_state[f"{key_prefix}_monthly"] = st.session_state[f"{key_prefix}_yearly"] / 12
    col1.number_input("Daily", min_value=0.0, step=0.01, key=f"{key_prefix}_daily", value=st.session_state[f"{key_prefix}_daily"], on_change=update_from_daily)
    col2.number_input("Monthly", min_value=0.0, step=0.01, key=f"{key_prefix}_monthly", value=st.session_state[f"{key_prefix}_monthly"], on_change=update_from_monthly)
    col3.number_input("Yearly", min_value=0.0, step=0.01, key=f"{key_prefix}_yearly", value=st.session_state[f"{key_prefix}_yearly"], on_change=update_from_yearly)
    return st.session_state[f"{key_prefix}_monthly"]

# Per-horse cost inputs
feed_monthly = feed_cost_block()
bedding_monthly = cost_block("Bedding", "bedding")  # Shavings or straw costs
water_monthly = cost_block("Water", "water")  # Variable water usage
electricity_monthly = cost_block("Electricity", "electricity")  # Variable electric usage
waste_disposal_monthly = cost_block("Waste Disposal", "waste_disposal")  # Manure removal

# Total per-horse costs
total_per_horse_monthly_cost = sum([feed_monthly, bedding_monthly, water_monthly, electricity_monthly, waste_disposal_monthly])
total_monthly_cost = total_per_horse_monthly_cost * total_horses
total_quarterly_cost = total_monthly_cost * 3
total_yearly_cost = total_monthly_cost * 12

# Cost summary
st.subheader("📊 Total Per-Horse Cost Summary")
col1, col2 = st.columns(2)
col1.metric("Number of Horses", f"{total_horses}")
col2.metric("Total Per-Horse Monthly Cost", f"€{total_per_horse_monthly_cost:,.2f}")
col1, col2, col3 = st.columns([1, 1, 1])
col1.metric("Total Monthly Cost", f"€{total_monthly_cost:,.2f}")
col2.metric("Total Quarterly Cost", f"€{total_quarterly_cost:,.2f}")
col3.metric("Total Yearly Cost", f"€{total_yearly_cost:,.2f}")

# --- Company Expenses ---
st.header("💰 Company Expenses")  # Miscellaneous business costs

# Company expense inputs
quarterly_maintenance_expense = expense_block("Maintenance", "maintenance", is_annual=True, include_description=True)  # Annual upkeep costs
quarterly_misc_expense = expense_block("Miscellaneous", "misc", is_annual=True, include_description=True)  # Other operational costs

# Total company expenses
total_quarterly_company_expense = quarterly_maintenance_expense + quarterly_misc_expense
total_monthly_company_expense = total_quarterly_company_expense / 3
total_annual_company_expense = total_quarterly_company_expense * 4

# Expenses summary
st.subheader("🏁 Total Company Expenses")
col1, col2, col3 = st.columns([1, 1, 1])
col1.metric("Monthly Total", f"€{total_monthly_company_expense:,.2f}")
col2.metric("Quarterly Total", f"€{total_quarterly_company_expense:,.2f}")
col3.metric("Annual Total", f"€{total_annual_company_expense:,.2f}")

# --- Calculations ---
monthly_income = monthly_occupancy_revenue + monthly_additional_revenue  # Total revenue
monthly_cost = total_monthly_cost + total_monthly_property_expense + total_monthly_company_expense  # Total expenses
monthly_profit = monthly_income - monthly_cost
current_quarter = monthly_profit * 3
projected_annual = monthly_profit * 12

# --- Quarterly Results & Year-End Summary ---
st.header("📊 Quarterly Results & Year-End Summary")

# Projected results
st.subheader("🟢 Projected Results (Auto-Calculated)")
col1, col2 = st.columns(2)
col1.metric("Projected Quarter Profit", f"€{current_quarter:,.2f}")
col2.metric("Projected Annual Profit", f"€{projected_annual:,.2f}")

# Manual quarterly inputs
st.subheader("📝 Enter Manual Results for Quarters 1–4")
col1, col2, col3, col4 = st.columns(4)
manual_q1 = col1.number_input("Quarter 1 Profit", min_value=0.0, step=100.0)
manual_q2 = col2.number_input("Quarter 2 Profit", min_value=0.0, step=100.0)
manual_q3 = col3.number_input("Quarter 3 Profit", min_value=0.0, step=100.0)
manual_q4 = col4.number_input("Quarter 4 Profit", min_value=0.0, step=100.0)

# Manual total
four_quarter_total = sum([manual_q1, manual_q2, manual_q3, manual_q4])
st.subheader("📅 4/4 Calculation")
st.metric("Total of Manual Quarters", f"€{four_quarter_total:,.2f}")
