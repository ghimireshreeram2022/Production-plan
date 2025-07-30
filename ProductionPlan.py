import streamlit as st
import pandas as pd
from auth import login  # Import your Supabase login function

# 🔐 Supabase Login Block
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔐 Salmonometer Production Plan Login")
    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    if st.button("Login"):
        user = login(email, password)
        if user:
            st.session_state["authenticated"] = True
            st.rerun()
    st.stop()

# ✅ App starts here after login
st.title("🐟 Salmonometer - Production Plan")

# Sidebar Plan Selection
plan_type = st.sidebar.selectbox(
    "Select Production Plan Type:",
    ("0+ Smolt Plan", "1+ Smolt Plan", "Ongrowing/Netpen Plan")
)

# Sidebar Inputs (Shared Base Inputs)
st.sidebar.header("📥 Input Parameters")

num_fish = st.sidebar.number_input("Number of Fish", min_value=100000, value=6000000, step=100000)
initial_weight = st.sidebar.number_input("Initial Weight (g)", min_value=0.1, value=0.2, step=0.1)
target_weight = st.sidebar.number_input("Target Weight (g)", min_value=1.0, value=100, step=10.0)
stocking_month = st.sidebar.selectbox("Stocking Month", [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
])
duration_months = st.sidebar.slider("Production Duration (months)", 6, 24, 14)
fcr = st.sidebar.number_input("Feed Conversion Ratio (FCR)", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
mortality_rate = st.sidebar.number_input("Monthly Mortality Rate (%)", min_value=0.0, max_value=100.0, value=1.0, step=0.1)

# Temperature Profile Input
st.sidebar.markdown("### 🌡️ Temperature Profile (°C)")
default_temp = [7.5]*12
temperature_profile = st.sidebar.text_area("Comma-separated temperatures (12 months):", value=",".join(map(str, default_temp)))
temperature_list = list(map(float, temperature_profile.split(","))) if temperature_profile else default_temp

# Display the selected plan and inputs
st.subheader(f"Selected Plan: {plan_type}")
st.write("### Input Summary:")
st.write({
    "Number of Fish": num_fish,
    "Initial Weight (g)": initial_weight,
    "Target Weight (g)": target_weight,
    "Stocking Month": stocking_month,
    "Duration (months)": duration_months,
    "FCR": fcr,
    "Mortality Rate (%)": mortality_rate,
    "Temperature Profile (°C)": temperature_list
})

# 🚪 Logout Button
if st.button("🚪 Logout"):
    st.session_state["authenticated"] = False
    st.rerun()
