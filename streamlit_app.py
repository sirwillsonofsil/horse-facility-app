import streamlit as st

# Set page configuration for the dashboard
st.set_page_config(page_title="Gelbstein Ranch Profitability Dashboard", layout="wide")
# Display the dashboard title with cactus emojis for a ranch theme
st.title("🌵 Gelbstein Ranch Profitability Dashboard 🌵")

# Initialize revenue variables to 0.0 to prevent NameError if inputs fail to initialize
monthly_occupancy_revenue = 0.0  # Monthly revenue from boarding horses
monthly_additional_revenue = 0.0  # Monthly revenue from additional services (e.g., lessons, rides)

# --- Property Expenses Inputs ---
# This section tracks fixed property-related costs (insurance, rent, electricity, water)
st.header("🏠 Property Expenses")

# Function to handle expense inputs with flexible time modes (Annual, Quarterly, Monthly)
# Args: label (str) - Name of the expense (e.g., "Insurance")
#       key_prefix (str) - Unique identifier for Streamlit input keys
# Returns: quarterly (float) - Expense converted to quarterly amount
def expense_block(label, key_prefix):
    col1, col2 = st.columns([1, 1.5])  # Create two columns for input mode and value
    mode = col1.selectbox("Input Mode", ["Annual", "Quarterly", "Monthly"], key=f"{key_prefix}_mode")  # Select time mode
    value = col2.number_input(f"{label}", min_value=0.0, step=100.0, key=f"{key_prefix}_value")  # Input expense value
    if mode == "Annual":
        quarterly = value / 4  # Convert annual to quarterly by dividing by 4
    elif mode == "Monthly":
        quarterly = value * 3  # Convert monthly to quarterly by multiplying by 3
    else:
        quarterly = value  # Quarterly input is used directly
    return quarterly

# Collect property expense inputs
q_insurance = expense_block("Insurance", "insurance")  # Quarterly insurance cost
q_rent = expense_block("Rent", "rent")  # Quarterly rent cost
q_electric = expense_block("Base Electric", "electric")  # Quarterly electricity cost
q_water = expense_block("Base Water", "water")  # Quarterly water cost

# Calculate total property expenses
total_quarterly_property_expense = q_insurance + q_rent + q_electric + q_water  # Sum of quarterly expenses
total_monthly_property_expense = total_quarterly_property_expense / 3  # Monthly expense for summary
total_annual_property_expense = total_quarterly_property_expense * 4  # Annual expense for summary

# Display property expenses summary
st.subheader("🏁 Total Property Expenses")
col1, col2, col3 = st.columns([1, 1, 1])  # Three columns for monthly, quarterly, annual totals
col1.metric("Monthly Total", f"€{total_monthly_property_expense:,.2f}")  # Monthly total in euros
col2.metric("Quarterly Total", f"€{total_quarterly_property_expense:,.2f}")  # Quarterly total in euros
col3.metric("Annual Total", f"€{total_annual_property_expense:,.2f}")  # Annual total in euros

# --- Occupancy Inputs ---
# This section tracks horse boarding details, including stall capacity and revenue from paying horses
st.header("🐎 Occupancy")
# First row for total stalls and company horses (non-paying) to conserve space
col1, col2 = st.columns([1.5, 1.5])
total_stalls = col1.number_input("Total Stalls", min_value=0, step=1, key="total_stalls")  # Total available stalls
company_horses = col2.number_input("Company Horses", min_value=0, step=1, key="company_horses")  # Non-paying company horses

# Separate rows for paying horse categories with count and monthly price
col1, col2 = st.columns([1, 1])
open_barn_horses = col1.number_input("Open Barn Horses", min_value=0, step=1, key="open_barn_horses")  # Horses not using fixed stalls
open_barn_horses_price = col2.number_input("Price (Per Month)", min_value=0.0, step=10.0, key="open_barn_horses_price")  # Monthly price per open barn horse

col1, col2 = st.columns([1, 1])
fullboard_training = col1.number_input("Fullboard Training", min_value=0, step=1, key="fullboard_training")  # Horses in fullboard training
fullboard_training_price = col2.number_input("Price (Per Month)", min_value=0.0, step=10.0, key="fullboard_training_price")  # Monthly price per fullboard horse

col1, col2 = st.columns([1, 1])
half_board = col1.number_input("Half Board", min_value=0, step=1, key="half_board")  # Horses in half board
half_board_price = col2.number_input("Price (Per Month)", min_value=0.0, step=10.0, key="half_board_price")  # Monthly price per half board horse

col1, col2 = st.columns([1, 1])
retirement_recovery_horse = col1.number_input("Retirement/Recovery Horse", min_value=0, step=1, key="retirement_recovery_horse")  # Retired or recovering horses
retirement_recovery_horse_price = col2.number_input("Price (Per Month)", min_value=0.0, step=10.0, key="retirement_recovery_horse_price")  # Monthly price per retired/recovering horse

# Occupancy Calculations
# Total horses includes all categories for tracking
total_horses = fullboard_training + half_board + company_horses + retirement_recovery_horse + open_barn_horses
# Remaining stalls excludes Open Barn Horses, as they don’t occupy fixed stalls
remaining_stalls = total_stalls - (fullboard_training + half_board + company_horses + retirement_recovery_horse)
# Monthly revenue from paying horses (excludes Company Horses)
monthly_occupancy_revenue = (
    fullboard_training * fullboard_training_price +
    half_board * half_board_price +
    retirement_recovery_horse * retirement_recovery_horse_price +
    open_barn_horses * open_barn_horses_price
)
quarterly_occupancy_revenue = monthly_occupancy_revenue * 3  # Quarterly revenue
annual_occupancy_revenue = monthly_occupancy_revenue * 12  # Annual revenue

# Display occupancy summary
st.subheader("📊 Occupancy Summary")
col1, col2 = st.columns(2)
col1.metric("Total Horses", f"{total_horses}")  # Total number of horses
col2.metric("Remaining Stalls", f"{remaining_stalls}")  # Available fixed stalls
col1, col2, col3 = st.columns([1, 1, 1])  # Three columns for revenue totals
col1.metric("Monthly Occupancy Revenue", f"€{monthly_occupancy_revenue:,.2f}")  # Monthly revenue
col2.metric("Quarterly Occupancy Revenue", f"€{quarterly_occupancy_revenue:,.2f}")  # Quarterly revenue
col3.metric("Annual Occupancy Revenue", f"€{annual_occupancy_revenue:,.2f}")  # Annual revenue

# --- Company Revenue Inputs ---
# This section tracks additional revenue from services like lessons, guest activities, and rides
st.header("💵 Company Revenue")

# Input rows for service counts and prices
col1, col2 = st.columns([1, 1])
ivanka_private_count = col1.number_input("Ivanka Private Lessons", min_value=0, step=1, key="ivanka_private_count")  # Number of private lessons
ivanka_private_price = col2.number_input("Price (Per Session)", min_value=0.0, step=10.0, key="ivanka_private_price")  # Price per private lesson

col1, col2 = st.columns([1, 1])
ivanka_group_count = col1.number_input("Ivanka Group Lessons", min_value=0, step=1, key="ivanka_group_count")  # Number of group lessons
ivanka_group_price = col2.number_input("Price (Per Session)", min_value=0.0, step=10.0, key="ivanka_group_price")  # Price per group lesson

col1, col2 = st.columns([1, 1])
kerry_mobile_count = col1.number_input("Kerry Mobile Sessions", min_value=0, step=1, key="kerry_mobile_count")  # Number of mobile sessions
kerry_mobile_price = col2.number_input("Price (Per Session)", min_value=0.0, step=10.0, key="kerry_mobile_price")  # Price per mobile session

col1, col2 = st.columns([1, 1])
parkour_guests_count = col1.number_input("Parkour Guests", min_value=0, step=1, key="parkour_guests_count")  # Number of parkour guests
parkour_guests_price = col2.number_input("Price (Per Guest)", min_value=0.0, step=10.0, key="parkour_guests_price")  # Price per parkour guest

col1, col2 = st.columns([1, 1])
horse_hotel_count = col1.number_input("Horse Hotel Guest Stays", min_value=0, step=1, key="horse_hotel_count")  # Number of horse hotel nights
horse_hotel_price = col2.number_input("Price (Per Night)", min_value=0.0, step=10.0, key="horse_hotel_price")  # Price per night

col1, col2 = st.columns([1, 1])
led_rides_count = col1.number_input("Led Pony Rides", min_value=0, step=1, key="led_rides_count")  # Number of pony rides
led_rides_price = col2.number_input("Price (Per Half Hour)", min_value=0.0, step=10.0, key="led_rides_price")  # Price per half-hour ride

# Company Revenue Calculations
# Monthly revenue from all services, assuming counts are per month
monthly_additional_revenue = (
    ivanka_private_count * ivanka_private_price +
    ivanka_group_count * ivanka_group_price +
    kerry_mobile_count * kerry_mobile_price +
    parkour_guests_count * parkour_guests_price +
    horse_hotel_count * horse_hotel_price +
    led_rides_count * led_rides_price
)
quarterly_additional_revenue = monthly_additional_revenue * 3  # Quarterly revenue
annual_additional_revenue = monthly_additional_revenue * 12  # Annual revenue

# Display company revenue summary
st.subheader("📊 Total Added Revenue")
col1, col2, col3 = st.columns([1, 1, 1])  # Three columns for revenue totals
col1.metric("Monthly Total Revenue", f"€{monthly_additional_revenue:,.2f}")  # Monthly revenue
col2.metric("Quarterly Total Revenue", f"€{quarterly_additional_revenue:,.2f}")  # Quarterly revenue
col3.metric("Annual Total Revenue", f"€{annual_additional_revenue:,.2f}")  # Annual revenue

# --- Per-Horse Costs ---
# This section tracks variable costs per horse (feed, bedding, water, electricity, waste disposal)
st.header("🐎 Per-Horse Costs")

# Function to calculate feed cost based on bale type, price, and number of horses fed
# Returns: monthly_cost_per_horse (float) - Monthly feed cost per horse
def feed_cost_block():
    st.subheader("Feed")
    col1, col2, col3 = st.columns([1, 1, 1])  # Three columns for inputs
    
    # Select bale type (affects cost calculation, currently treated as a label)
    bale_type = col1.selectbox("Bale Type", ["Square Bales", "Round Bales"], key="feed_bale_type")
    # Input price per bale in euros
    price_per_bale = col2.number_input("Price Per Bale (€)", min_value=0.0, step=1.0, key="feed_price_per_bale")
    # Input number of horses one bale feeds per month (defaults to 1 to avoid division by zero)
    horses_fed_per_month = col3.number_input("Horses Fed Per Month", min_value=1, step=1, key="feed_horses_fed", value=1)
    
    # Calculate monthly cost per horse: one bale’s cost divided by number of horses it feeds
    if horses_fed_per_month > 0:
        monthly_cost_per_horse = price_per_bale / horses_fed_per_month
    else:
        monthly_cost_per_horse = 0.0
    
    # Derive daily and yearly costs for display
    daily_cost_per_horse = monthly_cost_per_horse / 30  # Assuming 30 days per month
    yearly_cost_per_horse = monthly_cost_per_horse * 12  # 12 months per year
    
    # Display feed cost totals
    col1, col2, col3 = st.columns([1, 1, 1])  # Three columns for cost metrics
    col1.metric("Daily Cost Per Horse", f"€{daily_cost_per_horse:,.2f}")  # Daily cost in euros
    col2.metric("Monthly Cost Per Horse", f"€{monthly_cost_per_horse:,.2f}")  # Monthly cost in euros
    col3.metric("Yearly Cost Per Horse", f"€{yearly_cost_per_horse:,.2f}")  # Yearly cost in euros
    
    return monthly_cost_per_horse

# Function for other per-horse costs with daily, monthly, yearly inputs and real-time updates
# Args: label (str) - Cost category (e.g., "Bedding")
#       key_prefix (str) - Unique identifier for Streamlit input keys
# Returns: monthly (float) - Monthly cost per horse
def cost_block(label, key_prefix):
    st.subheader(label)
    col1, col2, col3 = st.columns([1, 1, 1])  # Three columns for inputs
    
    # Initialize session state to store input values
    if f"{key_prefix}_daily" not in st.session_state:
        st.session_state[f"{key_prefix}_daily"] = 0.0
        st.session_state[f"{key_prefix}_monthly"] = 0.0
        st.session_state[f"{key_prefix}_yearly"] = 0.0

    # Callback functions to update other inputs when one changes
    def update_from_daily():
        st.session_state[f"{key_prefix}_monthly"] = st.session_state[f"{key_prefix}_daily"] * 30  # Daily to monthly
        st.session_state[f"{key_prefix}_yearly"] = st.session_state[f"{key_prefix}_daily"] * 365  # Daily to yearly

    def update_from_monthly():
        st.session_state[f"{key_prefix}_daily"] = st.session_state[f"{key_prefix}_monthly"] / 30  # Monthly to daily
        st.session_state[f"{key_prefix}_yearly"] = st.session_state[f"{key_prefix}_monthly"] * 12  # Monthly to yearly

    def update_from_yearly():
        st.session_state[f"{key_prefix}_daily"] = st.session_state[f"{key_prefix}_yearly"] / 365  # Yearly to daily
        st.session_state[f"{key_prefix}_monthly"] = st.session_state[f"{key_prefix}_yearly"] / 12  # Yearly to monthly

    # Daily input with callback to update others
    daily = col1.number_input("Daily", min_value=0.0, step=0.01, key=f"{key_prefix}_daily", value=st.session_state[f"{key_prefix}_daily"], on_change=update_from_daily)

    # Monthly input with callback to update others
    monthly = col2.number_input("Monthly", min_value=0.0, step=0.01, key=f"{key_prefix}_monthly", value=st.session_state[f"{key_prefix}_monthly"], on_change=update_from_monthly)

    # Yearly input with callback to update others
    yearly = col3.number_input("Yearly", min_value=0.0, step=0.01, key=f"{key_prefix}_yearly", value=st.session_state[f"{key_prefix}_yearly"], on_change=update_from_yearly)

    return st.session_state[f"{key_prefix}_monthly"]

# Collect per-horse costs
feed_monthly = feed_cost_block()  # Monthly feed cost per horse
bedding_monthly = cost_block("Bedding", "bedding")  # Monthly bedding cost per horse
water_monthly = cost_block("Water", "water")  # Monthly water cost per horse
electricity_monthly = cost_block("Electricity", "electricity")  # Monthly electricity cost per horse
waste_disposal_monthly = cost_block("Waste Disposal", "waste_disposal")  # Monthly waste disposal cost per horse

# Total Per-Horse Cost Summary
# Calculate total costs per horse and for all horses
total_per_horse_monthly_cost = feed_monthly + bedding_monthly + water_monthly + electricity_monthly + waste_disposal_monthly  # Sum of monthly costs per horse
total_monthly_cost = total_per_horse_monthly_cost * total_horses  # Total monthly cost for all horses
total_quarterly_cost = total_monthly_cost * 3  # Total quarterly cost
total_yearly_cost = total_monthly_cost * 12  # Total yearly cost

# Display per-horse cost summary
st.subheader("📊 Total Per-Horse Cost Summary")
col1, col2 = st.columns(2)
col1.metric("Number of Horses", f"{total_horses}")  # Total number of horses from Occupancy
col2.metric("Total Per-Horse Monthly Cost", f"€{total_per_horse_monthly_cost:,.2f}")  # Monthly cost per horse
col1, col2, col3 = st.columns([1, 1, 1])  # Three columns for total costs
col1.metric("Total Monthly Cost", f"€{total_monthly_cost:,.2f}")  # Total monthly cost
col2.metric("Total Quarterly Cost", f"€{total_quarterly_cost:,.2f}")  # Total quarterly cost
col3.metric("Total Yearly Cost", f"€{total_yearly_cost:,.2f}")  # Total yearly cost

# --- Company Expenses ---
# This section tracks miscellaneous business expenses (maintenance, other costs)
st.header("💰 Company Expenses")

# Function to handle annual expense inputs with description
# Args: label (str) - Name of the expense (e.g., "Maintenance")
#       key_prefix (str) - Unique identifier for Streamlit input keys
# Returns: quarterly (float) - Expense converted to quarterly amount
def annual_expense_block(label, key_prefix):
    col1, col2 = st.columns([1.5, 2])  # Two columns for value and description
    value = col1.number_input(f"{label}", min_value=0.0, step=100.0, key=f"{key_prefix}_value")  # Input annual expense
    description = col2.text_input("Description", key=f"{key_prefix}_description")  # Optional description
    quarterly = value / 4  # Convert annual to quarterly
    return quarterly

# Collect company expense inputs
q_maintenance = annual_expense_block("Maintenance", "maintenance")  # Quarterly maintenance cost
q_misc = annual_expense_block("Miscellaneous", "misc")  # Quarterly miscellaneous cost

# Calculate total company expenses
total_quarterly_company_expense = q_maintenance + q_misc  # Sum of quarterly expenses
total_monthly_company_expense = total_quarterly_company_expense / 3  # Monthly expense for summary
total_annual_company_expense = total_quarterly_company_expense * 4  # Annual expense for summary

# Display company expenses summary
st.subheader("🏁 Total Company Expenses")
col1, col2, col3 = st.columns([1, 1, 1])  # Three columns for monthly, quarterly, annual totals
col1.metric("Monthly Total", f"€{total_monthly_company_expense:,.2f}")  # Monthly total in euros
col2.metric("Quarterly Total", f"€{total_quarterly_company_expense:,.2f}")  # Quarterly total in euros
col3.metric("Annual Total", f"€{total_annual_company_expense:,.2f}")  # Annual total in euros

# --- Calculations ---
# Calculate overall financial metrics
monthly_income = monthly_occupancy_revenue + monthly_additional_revenue  # Total monthly revenue
monthly_cost = (
    total_monthly_cost +  # Total per-horse costs (already multiplied by total_horses)
    (total_quarterly_property_expense + total_quarterly_company_expense) / 3  # Monthly property and company expenses
)
monthly_profit = monthly_income - monthly_cost  # Monthly profit
current_quarter = monthly_profit * 3  # Quarterly profit projection
projected_annual = monthly_profit * 12  # Annual profit projection

# --- Quarterly Results & Year-End Summary ---
# This section displays projected and manual profit results
st.header("📊 Quarterly Results & Year-End Summary")

# Display projected profits
st.subheader("🟢 Projected Results (Auto-Calculated)")
col1, col2 = st.columns(2)
col1.metric("Projected Quarter Profit", f"€{current_quarter:,.2f}")  # Projected quarterly profit
col2.metric("Projected Annual Profit", f"€{projected_annual:,.2f}")  # Projected annual profit

# Input manual quarterly profits
st.subheader("📝 Enter Manual Results for Quarters 1–4")
col1, col2, col3, col4 = st.columns(4)  # Four columns for quarterly inputs
manual_q1 = col1.number_input("Quarter 1 Profit", min_value=0.0, step=100.0)  # Q1 profit
manual_q2 = col2.number_input("Quarter 2 Profit", min_value=0.0, step=100.0)  # Q2 profit
manual_q3 = col3.number_input("Quarter 3 Profit", min_value=0.0, step=100.0)  # Q3 profit
manual_q4 = col4.number_input("Quarter 4 Profit", min_value=0.0, step=100.0)  # Q4 profit

# Calculate and display total of manual quarters
four_quarter_total = manual_q1 + manual_q2 + manual_q3 + manual_q4  # Sum of manual profits
st.subheader("📅 4/4 Calculation")
st.metric("Total of Manual Quarters", f"€{four_quarter_total:,.2f}")  # Total in euros
