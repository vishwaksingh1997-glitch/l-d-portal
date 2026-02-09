import streamlit as st
import pandas as pd

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Login | SSI Learning & Development",
    layout="wide"
)

# ==================================================
# SESSION INIT
# ==================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "user_role" not in st.session_state:
    st.session_state.user_role = None

# ==================================================
# LOAD USERS (FROM STREAMLIT SECRETS)
# ==================================================
@st.cache_data
def load_users():
    users = st.secrets["users"]

    df = pd.DataFrame({
        "email": users["email"],
        "password": users["password"],
        "role": users["role"]
    })

    df["email"] = df["email"].astype(str).str.strip()
    df["password"] = df["password"].astype(str).str.strip()
    df["role"] = df["role"].astype(str).str.strip().str.lower()

    return df

users_df = load_users()


# ==================================================
# GLOBAL THEME (SAME AS HOME)
# ==================================================
st.markdown("""
<style>
.stApp {
    background-color: #ADD8E6;
}

/* Header */
[data-testid="stHeader"] {
    background: linear-gradient(180deg, #0B3C5D, #06283D);
}
[data-testid="stHeader"] * {
    color: white !important;
}

/* Sidebar (hidden visually but keeps layout consistent) */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B3C5D, #07263D);
}

/* Login Card */
.login-card {
    background: white;
    padding: 45px;
    border-radius: 20px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.25);
    max-width: 420px;
    margin: 80px auto;
}

.login-title {
    text-align: center;
    font-size: 30px;
    font-weight: 800;
    color: #0B3C5D;
    margin-bottom: 25px;
}

.login-subtitle {
    text-align: center;
    color: #555;
    margin-bottom: 25px;
}

.stButton button {
    background-color: #1F77B4;
    color: white;
    font-weight: 600;
    border-radius: 10px;
    width: 100%;
    padding: 12px;
}

.stButton button:hover {
    background-color: #155A8A;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# HEADER BANNER (SAME IMAGE AS HOME)
# ==================================================
st.markdown("""
<div class="header-banner" style="
    background:
        linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)),
        url('https://ssinnovations.com/wp-content/uploads/2025/07/SSI-M3-Home-Splash-MAR25-v3.webp');
    background-size: cover;
    background-position: center;
    border-radius: 22px;
    padding: 60px 40px;
    color: white;
    text-align: center;
    margin-bottom: 40px;
">
    <h1>SSI Learning & Development</h1>
    <p>Secure access to training dashboards and resources</p>
</div>
""", unsafe_allow_html=True)

# ==================================================
# LOGIN CARD
# ==================================================
st.markdown("""
<div class="login-card">
    <div class="login-title">🔐 Login</div>
    <div class="login-subtitle">Use your SSI credentials</div>
</div>
""", unsafe_allow_html=True)

email = st.text_input("Email")
password = st.text_input("Password", type="password")

# ==================================================
# LOGIN LOGIC
# ==================================================
if st.button("Login"):
    match = users_df[
        (users_df["email"] == email.strip()) &
        (users_df["password"] == password.strip())
    ]

    if not match.empty:
        st.session_state.logged_in = True
        st.session_state.user_email = match.iloc[0]["email"]
        st.session_state.user_role = match.iloc[0]["role"]

        st.success("Login successful")
        st.switch_page("pages/0_Home.py")

    else:
        st.error("Invalid email or password")
