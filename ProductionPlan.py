import streamlit as st
from supabase import create_client, Client

# Supabase configuration (put this at the top)
SUPABASE_URL = "https://phxybrgcyfcwaclhdmqy.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBoeHlicmdjeWZjd2FjbGhkbXF5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM4OTExOTUsImV4cCI6MjA2OTQ2NzE5NX0.PXU8JCN68gcQrZFLJp2omuUUq3QzW3WTDFU1jpM3Qgo"

# Initialize Supabase client
@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# Authentication check
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Login screen
if not st.session_state["authenticated"]:
    st.title("🔐 Salmonometer Production Plan Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        try:
            # Supabase authentication
            auth_response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            st.session_state["authenticated"] = True
            st.session_state["user"] = auth_response.user
            st.rerun()
        except Exception as e:
            st.error(f"Login failed: {e}")
    st.stop()

st.title("🐟 Salmonometer - Production Plan")

url = "https://phxybrgcyfcwaclhdmqy.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBoeHlicmdjeWZjd2FjbGhkbXF5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM4OTExOTUsImV4cCI6MjA2OTQ2NzE5NX0.PXU8JCN68gcQrZFLJp2omuUUq3QzW3WTDFU1jpM3Qgo"
supabase: Client = create_client(url, key)


# Sidebar Plan Selection
plan_type = st.sidebar.selectbox(
    "Select Production Plan Type:",
    ("0+ Smolt Plan", "1+ Smolt Plan", "Ongrowing/Netpen Plan")
)

# Sidebar Inputs (Shared Base Inputs)
st.sidebar.header("📥 Input Parameters")

num_fish = st.sidebar.number_input("Number of Fish", min_value=100000, value=6000000, step=100000)
initial_weight = st.sidebar.number_input("Initial Weight (g)", min_value=0.1, value=0.2, step=0.1)
target_weight = st.sidebar.number_input("Target Weight (g)", min_value=1.0, value=100.0, step=10.0)
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
