"""
Bharat Yatra: India Tourist Cities Travel Cost Calculator & AI Planner.
Full Web Platform featuring User Dashboard, Authentication (Sign In, Sign Up, Forgot Password with Resend OTP),
Trip Cost Calculator, AI Day-by-Day Itinerary, and 24/7 AI Travel Copilot.
"""

import os
from datetime import datetime, date, timedelta
import pandas as pd
import streamlit as st

from travel_calculator import (
    load_india_tourist_data,
    load_india_routes_data,
    get_unique_states,
    get_cities_by_state,
    get_city_details,
    estimate_intercity_fare,
    calculate_trip_budget,
    format_inr,
    generate_trip_summary_text
)
from ai_planner import (
    generate_fast_ai_trip_plan,
    generate_ai_itinerary,
    generate_ai_budget_tips,
    ask_ai_travel_copilot
)
from auth import (
    register_user,
    authenticate_user,
    send_password_reset_otp,
    verify_otp_and_reset_password,
    save_user_trip,
    get_user_saved_trips,
    delete_user_saved_trip
)
from data import (
    ORIGIN_HUBS,
    TRAVEL_STYLES,
    TRAVEL_MODES
)

# Page Configuration
st.set_page_config(
    page_title="Bharat Yatra | India Travel Planner & Dashboard",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for modern website aesthetic
st.markdown("""
<style>
    /* Hide Streamlit Deploy button, header toolbar and footer */
    header {visibility: hidden !important; display: none !important;}
    [data-testid="stToolbar"] {visibility: hidden !important; display: none !important;}
    .stDeployButton {display: none !important;}
    footer {visibility: hidden !important; display: none !important;}
    #MainMenu {visibility: hidden !important; display: none !important;}

    /* Modern Light Nature Palette */
    .stApp {
        background-color: #FAFAF7 !important;
    }
    .brand-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1B4332;
        margin-bottom: 3px;
        letter-spacing: -0.5px;
    }
    .brand-sub {
        font-size: 1.0rem;
        color: #406353;
        margin-bottom: 1.4rem;
    }
    .auth-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 32px;
        box-shadow: 0 4px 20px -2px rgba(45, 106, 79, 0.06);
        max-width: 480px;
        margin: 0 auto;
    }
    .dashboard-stat-card {
        background: linear-gradient(135deg, #F0FDF4 0%, #E8F5E9 100%);
        border: 1px solid #C8E6C9;
        border-radius: 16px;
        padding: 22px;
        text-align: center;
    }
    .summary-card {
        background: linear-gradient(135deg, #F2F8F4 0%, #E7EFE9 100%);
        border: 1px solid #C8DEC9;
        border-radius: 16px;
        padding: 20px 24px;
        margin: 16px 0;
    }
    .summary-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1B4332;
        margin-bottom: 8px;
    }
    .summary-text {
        font-size: 1.02rem;
        color: #2D6A4F;
        line-height: 1.6;
    }
    .info-badge {
        background-color: #F0FDF4;
        border-radius: 14px;
        padding: 16px 20px;
        border-left: 5px solid #2D6A4F;
        margin: 14px 0;
        color: #1B4332;
        font-size: 0.95rem;
    }
    .nature-day-card {
        background: #FFFFFF;
        border: 1px solid #E2EAE4;
        border-radius: 16px;
        padding: 22px 26px;
        margin-bottom: 18px;
        box-shadow: 0 4px 16px -2px rgba(45, 106, 79, 0.05);
        border-left: 6px solid #2D6A4F;
    }
    .stButton>button {
        background-color: #2D6A4F;
        color: #FFFFFF;
        font-weight: 600;
        border-radius: 10px;
        border: none;
        padding: 0.6rem 1.8rem;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #1B4332;
        color: #FFFFFF;
        box-shadow: 0 4px 14px rgba(45, 106, 79, 0.25);
    }
    [data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E3ECE4;
        border-radius: 14px;
        padding: 14px 18px;
        box-shadow: 0 2px 10px rgba(45, 106, 79, 0.04);
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_datasets():
    tourist_df = load_india_tourist_data()
    routes_df = load_india_routes_data()
    return tourist_df, routes_df


def init_session_state():
    """Ensure persistent session variables."""
    if "user" not in st.session_state:
        st.session_state["user"] = None
    if "nav_page" not in st.session_state:
        st.session_state["nav_page"] = "Dashboard" if st.session_state["user"] else "Sign In"
    if "gemini_api_key" not in st.session_state:
        g_key = ""
        try:
            g_key = st.secrets.get("GEMINI_API_KEY", "")
        except Exception:
            pass
        st.session_state["gemini_api_key"] = g_key or os.environ.get("GEMINI_API_KEY", "")
    if "resend_api_key" not in st.session_state:
        r_key = ""
        try:
            r_key = st.secrets.get("RESEND_API_KEY", "")
        except Exception:
            pass
        st.session_state["resend_api_key"] = r_key or os.environ.get("RESEND_API_KEY", "")


def render_sidebar():
    """Render modern sidebar with navigation and user profile status."""
    st.sidebar.image("https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=600&q=80", use_container_width=True)
    st.sidebar.markdown("### 🇮🇳 Bharat Yatra")
    st.sidebar.caption("India Tourist Travel Calculator & AI Planner")
    st.sidebar.markdown("---")

    user = st.session_state.get("user")

    if user:
        st.sidebar.markdown(f"👤 **Hello, {user['name']}!**")
        st.sidebar.caption(f"Logged in as `{user['email']}`")
        
        pages = [
            "📊 Dashboard",
            "🧮 Trip Calculator",
            "🌿 AI Travel Studio",
            "🗺️ Explore 45+ Destinations",
            "🚪 Logout"
        ]
        chosen = st.sidebar.radio("Navigation", pages, index=pages.index(st.session_state.get("nav_page", "📊 Dashboard")) if st.session_state.get("nav_page") in pages else 0)
        
        if chosen == "🚪 Logout":
            st.session_state["user"] = None
            st.session_state["nav_page"] = "🔐 Sign In"
            st.rerun()
        else:
            st.session_state["nav_page"] = chosen
    else:
        st.sidebar.markdown("🔒 **Account Access**")
        guest_pages = [
            "🔐 Sign In",
            "📝 Create Account",
            "🔑 Forgot Password",
            "🧮 Guest Trip Calculator",
            "🌿 AI Travel Studio",
            "🗺️ Explore 45+ Destinations"
        ]
        chosen = st.sidebar.radio("Navigation", guest_pages, index=guest_pages.index(st.session_state.get("nav_page", "🔐 Sign In")) if st.session_state.get("nav_page") in guest_pages else 0)
        st.session_state["nav_page"] = chosen

    st.sidebar.markdown("---")
    st.sidebar.caption("🌿 Bharat Yatra v2.0 • Plan your dream India trip")


# =====================================================================
# VIEW: SIGN IN
# =====================================================================
def view_login():
    st.markdown('<div class="brand-title">🔐 Sign In to Bharat Yatra</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">Access your personal dashboard, saved trips, and AI itineraries.</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        with st.form("login_form"):
            email = st.text_input("Email Address", placeholder="name@example.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submit = st.form_submit_button("Sign In", use_container_width=True)

            if submit:
                success, user_data, msg = authenticate_user(email, password)
                if success:
                    st.session_state["user"] = user_data
                    st.session_state["nav_page"] = "📊 Dashboard"
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

        c1, c2 = st.columns(2)
        if c1.button("🔑 Forgot Password?"):
            st.session_state["nav_page"] = "🔑 Forgot Password"
            st.rerun()
        if c2.button("📝 Create New Account"):
            st.session_state["nav_page"] = "📝 Create Account"
            st.rerun()

        st.markdown("---")
        st.markdown("**⚡ Quick Test?**")
        if st.button("🚀 1-Click Demo Login (Amaan Demo)", use_container_width=True):
            st.session_state["user"] = {"id": 1, "name": "Amaan Demo", "email": "demo@yatra.com"}
            st.session_state["nav_page"] = "📊 Dashboard"
            st.rerun()


# =====================================================================
# VIEW: SIGN UP
# =====================================================================
def view_signup():
    st.markdown('<div class="brand-title">📝 Create Your Account</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">Join thousands of travelers planning domestic Indian holidays with AI.</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        with st.form("signup_form"):
            name = st.text_input("Full Name", placeholder="e.g. Amaan Khan")
            email = st.text_input("Email Address", placeholder="name@example.com")
            password = st.text_input("Password (min 6 characters)", type="password", placeholder="••••••••")
            confirm_pwd = st.text_input("Confirm Password", type="password", placeholder="••••••••")
            submit = st.form_submit_button("Create Account", use_container_width=True)

            if submit:
                if password != confirm_pwd:
                    st.error("Passwords do not match!")
                else:
                    success, msg = register_user(name, email, password)
                    if success:
                        st.success(msg)
                        st.info("You can now sign in using your credentials.")
                    else:
                        st.error(msg)

        st.markdown("Already have an account?")
        if st.button("👉 Go to Sign In", use_container_width=True):
            st.session_state["nav_page"] = "🔐 Sign In"
            st.rerun()


# =====================================================================
# VIEW: FORGOT PASSWORD (WITH RESEND OTP)
# =====================================================================
def view_forgot_password():
    st.markdown('<div class="brand-title">🔑 Reset Your Password</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">Receive a secure 6-digit OTP to verify your email and set a new password.</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        # Step 1: Request OTP
        st.markdown("##### Step 1: Enter your registered email")
        email_input = st.text_input("Registered Email", placeholder="name@example.com", key="forgot_email")
        
        resend_key = st.session_state.get("resend_api_key", "")
        if not resend_key:
            st.caption("ℹ️ *Note: If Resend API key is not configured in Settings, a test demo OTP will be shown on-screen.*")

        if st.button("📨 Send Verification OTP", use_container_width=True):
            if not email_input:
                st.error("Please enter your email address.")
            else:
                success, msg, demo_otp = send_password_reset_otp(email_input, resend_key)
                if success:
                    st.success(msg)
                    st.session_state["otp_sent_to"] = email_input
                    if demo_otp:
                        st.warning(f"🧪 Demo Mode Verification Code: **{demo_otp}**")
                else:
                    st.error(msg)

        st.markdown("---")

        # Step 2: Verify & Reset
        st.markdown("##### Step 2: Enter OTP & New Password")
        with st.form("reset_pwd_form"):
            otp_val = st.text_input("6-Digit OTP Code", placeholder="123456", max_chars=6)
            new_pwd = st.text_input("New Password (min 6 characters)", type="password", placeholder="••••••••")
            confirm_new_pwd = st.text_input("Confirm New Password", type="password", placeholder="••••••••")
            reset_btn = st.form_submit_button("Reset Password", use_container_width=True)

            if reset_btn:
                target_email = st.session_state.get("otp_sent_to") or email_input
                if not target_email:
                    st.error("Please enter your email and request an OTP first.")
                elif new_pwd != confirm_new_pwd:
                    st.error("New passwords do not match.")
                else:
                    ok, r_msg = verify_otp_and_reset_password(target_email, otp_val, new_pwd)
                    if ok:
                        st.success(r_msg)
                        st.balloons()
                    else:
                        st.error(r_msg)

        if st.button("← Back to Sign In", use_container_width=True):
            st.session_state["nav_page"] = "🔐 Sign In"
            st.rerun()


# =====================================================================
# VIEW: USER DASHBOARD
# =====================================================================
def view_dashboard(tourist_df, routes_df):
    user = st.session_state.get("user")
    st.markdown(f'<div class="brand-title">📊 Travel Dashboard: Welcome, {user["name"]}!</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">Manage your saved trip budgets, view destinations, and plan your next journey across India.</div>', unsafe_allow_html=True)

    # Fetch user's saved trips
    saved_trips = get_user_saved_trips(user["email"])

    # Top Stat Cards
    c1, c2, c3 = st.columns(3)
    c1.metric("📁 Saved Trips", f"{len(saved_trips)}", "Planned Journeys")
    c2.metric("🇮🇳 Cities Covered", f"{len(tourist_df)}", "Available in Database")
    
    total_budget_sum = 0
    for trip in saved_trips:
        cleaned = trip["total_budget"].replace("₹", "").replace(",", "").strip()
        try:
            total_budget_sum += float(cleaned)
        except ValueError:
            pass
    c3.metric("💰 Total Planned Travel", format_inr(total_budget_sum), "Across all saved trips")

    st.markdown("---")

    # Quick Action Bar
    q1, q2 = st.columns([3, 1])
    q1.subheader("🧳 Your Saved Trips History")
    if q2.button("➕ Plan a New Trip", use_container_width=True):
        st.session_state["nav_page"] = "🧮 Trip Calculator"
        st.rerun()

    if not saved_trips:
        st.info("You haven't saved any trip estimates yet. Head over to the **Trip Calculator** to plan and save your first adventure!")
    else:
        for trip in saved_trips:
            with st.container():
                st.markdown(f"""
                <div class="summary-card" style="margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 1.25rem; font-weight: 700; color: #1E3A8A;">📍 {trip['destination']}</span>
                            <span style="color: #64748B; font-size: 0.95rem; margin-left: 10px;">(From {trip['origin']})</span>
                        </div>
                        <div style="font-size: 1.3rem; font-weight: 800; color: #FF6B35;">
                            {trip['total_budget']}
                        </div>
                    </div>
                    <div style="margin-top: 8px; color: #334155; font-size: 0.95rem;">
                        📅 <b>Dates:</b> {trip['travel_dates']} &nbsp;|&nbsp; 
                        👥 <b>Travelers:</b> {trip['travelers']} &nbsp;|&nbsp; 
                        🌟 <b>Style:</b> {trip['travel_style']} &nbsp;|&nbsp; 
                        👤 <b>Per Person:</b> {trip['cost_per_person']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons for this trip
                ac1, ac2 = st.columns([6, 1])
                with ac2:
                    if st.button("🗑️ Delete", key=f"del_{trip['id']}", use_container_width=True):
                        delete_user_saved_trip(trip["id"], user["email"])
                        st.success("Trip removed.")
                        st.rerun()


# =====================================================================
# VIEW: TRIP CALCULATOR
# =====================================================================
def view_calculator(tourist_df, routes_df):
    user = st.session_state.get("user")
    st.markdown('<div class="brand-title">🧮 India Tourist Trip Cost Calculator</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">Simple, accurate Indian domestic travel budgeting in Rupee (₹).</div>', unsafe_allow_html=True)

    st.markdown("#### 1️⃣ Plan Your Journey")
    c1, c2, c3 = st.columns(3)
    origin_city = c1.selectbox("✈️ Departure Hub (Origin)", ORIGIN_HUBS, index=0)

    all_cities = sorted(tourist_df["City"].unique().tolist())
    default_city_idx = all_cities.index("Jaipur") if "Jaipur" in all_cities else 0
    dest_city = c2.selectbox("🎯 Tourist Destination (Where to visit?)", all_cities, index=default_city_idx)

    city_info = get_city_details(tourist_df, dest_city)
    dest_state = city_info.get("State", "India")
    c3.text_input("📍 State / Region", value=dest_state, disabled=True)

    st.markdown("#### 2️⃣ Dates, Travelers & Style")
    d1, d2, d3, d4 = st.columns(4)
    today = date.today()
    start_date = d1.date_input("📅 Start Date", value=today + timedelta(days=14), min_value=today)
    end_date = d2.date_input("📅 End Date", value=today + timedelta(days=18), min_value=start_date)

    trip_days = max(1, (end_date - start_date).days + 1)
    trip_nights = max(1, (end_date - start_date).days) if trip_days > 1 else 1

    num_travelers = d3.number_input("👥 Travelers", min_value=1, max_value=50, value=2, step=1)
    suggested_rooms = max(1, (num_travelers + 1) // 2)
    num_rooms = d4.number_input("🏨 Rooms Needed", min_value=1, max_value=25, value=suggested_rooms, step=1)

    s1, s2 = st.columns(2)
    travel_style = s1.selectbox("🌟 Travel Style / Comfort", TRAVEL_STYLES, index=1)
    travel_mode = s2.selectbox("🚆 Inter-city Transport Mode", TRAVEL_MODES, index=1)

    # Automatic rate calculations
    if "Budget" in travel_style:
        default_hotel = float(city_info.get("Hotel_Budget_Night", 1200))
        default_food = float(city_info.get("Food_Budget_Day", 450))
        default_transit = float(city_info.get("Local_Transit_Budget_Day", 350))
    elif "Luxury" in travel_style:
        default_hotel = float(city_info.get("Hotel_Luxury_Night", 8500))
        default_food = float(city_info.get("Food_Luxury_Day", 2500))
        default_transit = float(city_info.get("Local_Transit_Luxury_Day", 2200))
    else:  # Standard
        default_hotel = float(city_info.get("Hotel_Standard_Night", 3200))
        default_food = float(city_info.get("Food_Standard_Day", 1100))
        default_transit = float(city_info.get("Local_Transit_Standard_Day", 900))

    default_sightseeing = float(city_info.get("Sightseeing_Est_Daily", 500))
    ow_fare, rt_fare, fare_note = estimate_intercity_fare(origin_city, dest_city, travel_mode, routes_df)

    # Optional fine-tuning expander
    with st.expander("⚙️ Fine-Tune Daily Rates (Optional - Verified Indian Database Averages)"):
        is_flat_car = "Car" in travel_mode or "Cab" in travel_mode
        fare_label = "Intercity Return Fuel+Tolls (Total Vehicle) (₹)" if is_flat_car else "Intercity Return Fare / Person (₹)"
        
        ar1, ar2, ar3 = st.columns(3)
        intercity_fare_val = ar1.number_input(fare_label, min_value=0.0, value=float(rt_fare), step=100.0, format="%.0f")
        hotel_rate_val = ar2.number_input("Hotel Rate / Night / Room (₹)", min_value=0.0, value=float(default_hotel), step=100.0, format="%.0f")
        food_rate_val = ar3.number_input("Food & Meals / Person / Day (₹)", min_value=0.0, value=float(default_food), step=50.0, format="%.0f")

        ar4, ar5, ar6 = st.columns(3)
        local_transit_val = ar4.number_input("Local Transit & Commute / Day (₹)", min_value=0.0, value=float(default_transit), step=50.0, format="%.0f")
        sightseeing_val = ar5.number_input("Sightseeing & Tickets / Person / Day (₹)", min_value=0.0, value=float(default_sightseeing), step=50.0, format="%.0f")
        buffer_pct = ar6.slider("Contingency & Emergency Buffer (%)", min_value=0, max_value=25, value=10, step=1)

    calc_btn = st.button("🚀 Calculate Trip Budget", use_container_width=True)

    # Execute calculation
    result = calculate_trip_budget(
        start_date=start_date,
        end_date=end_date,
        num_travelers=num_travelers,
        rooms_needed=num_rooms,
        travel_style=travel_style,
        intercity_fare_roundtrip=intercity_fare_val,
        intercity_mode=travel_mode,
        hotel_rate_per_night=hotel_rate_val,
        food_rate_per_day_per_person=food_rate_val,
        local_transit_per_day=local_transit_val,
        sightseeing_per_day_per_person=sightseeing_val,
        emergency_buffer_pct=buffer_pct
    )
    st.session_state["budget_result"] = result
    st.session_state["trip_meta"] = {
        "origin": origin_city,
        "city": dest_city,
        "state": dest_state,
        "start_date": start_date,
        "end_date": end_date,
        "city_info": city_info
    }

    # Summary Card
    st.markdown(f"""
    <div class="summary-card">
        <div class="summary-title">🎉 Trip Budget Estimate for {dest_city}, {dest_state}</div>
        <div class="summary-text">
            For <b>{num_travelers} traveler(s)</b> spending <b>{result['total_days']} days ({result['hotel_nights']} nights)</b> in <b>{dest_city}</b> 
            with <b>{travel_style.split('(')[0].strip()}</b> comfort traveling via <b>{travel_mode.split('(')[0].strip()}</b>, 
            your total estimated budget is <b>{result['fmt_grand_total']}</b> (approx <b>{result['fmt_cost_per_person']} per person</b>).
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("💰 Total Trip Budget", result["fmt_grand_total"], f"{result['total_days']} Days")
    m2.metric("👤 Cost Per Traveler", result["fmt_cost_per_person"], f"For {num_travelers} pax")
    m3.metric("📅 Daily Average Spend", result["fmt_cost_per_day"], "Per Day")
    m4.metric("🏨 Stay Duration", f"{result['hotel_nights']} Nights", f"{num_rooms} Room(s)")

    # Breakdown Table & Bar Chart
    b_col1, b_col2 = st.columns([1.1, 0.9], gap="large")

    with b_col1:
        st.markdown("##### 📋 Where will your money go?")
        breakdown_data = [
            {"Category": "🚆 Inter-city Transport", "Cost": result["fmt_intercity_total"], "Details": f"{travel_mode} ({origin_city} ⇄ {dest_city})"},
            {"Category": "🏨 Accommodation", "Cost": result["fmt_hotel_total"], "Details": f"{result['hotel_nights']} nights × {num_rooms} room(s)"},
            {"Category": "🍛 Food & Dining", "Cost": result["fmt_food_total"], "Details": f"{result['total_days']} days for {num_travelers} person(s)"},
            {"Category": "🛺 Local Commute", "Cost": result["fmt_local_transit_total"], "Details": f"Cabs / autos / scooty for {result['total_days']} days"},
            {"Category": "🎟️ Sightseeing & Activities", "Cost": result["fmt_sightseeing_total"], "Details": "Monument passes & local attractions"},
            {"Category": "🛡️ Emergency & Misc Buffer", "Cost": result["fmt_emergency_buffer"], "Details": f"{buffer_pct}% safety margin for shopping/buffer"},
        ]
        st.dataframe(
            pd.DataFrame(breakdown_data)[["Category", "Cost", "Details"]],
            use_container_width=True,
            hide_index=True
        )

    with b_col2:
        st.markdown("##### 📊 Expense Distribution")
        chart_data = {
            "Transport": result["intercity_total"],
            "Stay": result["hotel_total"],
            "Food": result["food_total"],
            "Commute": result["local_transit_total"],
            "Sightseeing": result["sightseeing_total"],
            "Buffer": result["emergency_buffer"]
        }
        st.bar_chart(pd.DataFrame(list(chart_data.items()), columns=["Expense", "Amount (₹)"]).set_index("Expense"), color="#FF6B35")

    # Save to Dashboard Button
    st.markdown("---")
    sv_col1, sv_col2 = st.columns([3, 1])
    if user:
        if sv_col1.button("💾 Save this Trip to My Dashboard", use_container_width=True):
            dates_str = f"{start_date.strftime('%d %b')} - {end_date.strftime('%d %b %Y')}"
            save_user_trip(
                user_email=user["email"],
                destination=f"{dest_city}, {dest_state}",
                origin=origin_city,
                travel_dates=dates_str,
                travelers=num_travelers,
                travel_style=travel_style.split('(')[0].strip(),
                total_budget=result["fmt_grand_total"],
                cost_per_person=result["fmt_cost_per_person"]
            )
            st.success("✅ Trip saved to your Dashboard!")
    else:
        sv_col1.info("💡 Want to save this trip to your account history? **Sign In** or **Create an Account** in the sidebar!")

    # Summary copy & download
    summary_txt = generate_trip_summary_text(
        city=dest_city,
        state=dest_state,
        start_date=start_date,
        end_date=end_date,
        costs=result
    )
    sv_col2.download_button(
        label="📥 Download Plan (.txt)",
        data=summary_txt,
        file_name=f"{dest_city}_Budget.txt",
        mime="text/plain",
        use_container_width=True
    )


# =====================================================================
# VIEW: AI TRAVEL STUDIO (UNIFIED ITINERARY & COPILOT)
# =====================================================================
def view_ai_studio():
    meta = st.session_state.get("trip_meta", {})
    res = st.session_state.get("budget_result", {})
    dest_city = meta.get("city", "Jaipur")
    dest_state = meta.get("state", "Rajasthan")
    city_info = meta.get("city_info", {})
    days = res.get("total_days", 4)
    travelers = res.get("num_travelers", 2)
    style = res.get("travel_style", "Standard / Family")
    api_key = st.session_state.get("gemini_api_key", "")

    st.markdown('<div class="brand-title">🌿 AI Travel Studio</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="brand-sub">Smart Day-by-Day Itineraries & 24/7 Travel Copilot for <b>{dest_city}, {dest_state}</b> ({days} Days • {travelers} Traveler(s)).</div>', unsafe_allow_html=True)

    tab_plan, tab_chat = st.tabs(["📅 Smart Day-by-Day Itinerary", "💬 YatraAI Copilot (24/7 Chat)"])

    with tab_plan:
        c1, c2 = st.columns([1.6, 2.4])
        ai_mode = c1.radio("Generation Speed:", ["🤖 Live Gemini AI (High Detail)", "⚡ Instant Mode (0.1s)"], horizontal=True)
        gen_btn = c2.button("✨ Generate Curated Itinerary & Hacks", use_container_width=True)

        if gen_btn:
            is_instant = "Instant" in ai_mode
            with st.spinner("Generating instant travel plan..." if is_instant else f"Connecting to Gemini AI for live custom plan for {dest_city}..."):
                itinerary_md, tips_md = generate_fast_ai_trip_plan(
                    city=dest_city,
                    state=dest_state,
                    days=days,
                    num_travelers=travelers,
                    travel_style=style,
                    intercity_mode=res.get("intercity_mode", "Train"),
                    grand_total=res.get("grand_total", 25000),
                    city_details=city_info,
                    api_key=api_key,
                    force_instant=is_instant
                )
                st.session_state["ai_itinerary"] = itinerary_md
                st.session_state["ai_tips"] = tips_md

        if "ai_itinerary" in st.session_state:
            st.markdown(st.session_state["ai_itinerary"])
            st.markdown("---")
            st.markdown("### 💡 AI Smart Money-Saving Hacks")
            st.markdown(st.session_state.get("ai_tips", ""))
            
            st.download_button(
                label="📥 Download Full Itinerary (.md)",
                data=f"{st.session_state['ai_itinerary']}\n\n## Cost-Saving Hacks\n{st.session_state.get('ai_tips', '')}",
                file_name=f"{dest_city}_{days}Days_AI_Itinerary.md",
                mime="text/markdown"
            )
        else:
            st.info(f"👆 Select your speed and click **'Generate Curated Itinerary & Hacks'** to create your plan for {dest_city}!")

    with tab_chat:
        st.markdown("##### Got questions about safety, food, or packing for this trip?")

        if "copilot_messages" not in st.session_state:
            st.session_state["copilot_messages"] = [
                {"role": "assistant", "content": f"Namaste! 🙏 I am your YatraAI Travel Assistant. How can I help you plan your journey to {dest_city}?"}
            ]

        # Quick prompts
        q1, q2, q3, q4 = st.columns(4)
        if q1.button("🎒 What to pack?"):
            st.session_state["prompt_input"] = f"What should I pack for my trip to {dest_city}?"
        if q2.button("🛡️ Is it safe for solo travel?"):
            st.session_state["prompt_input"] = f"Is {dest_city} safe for solo and women travelers?"
        if q3.button("🍛 Best street food?"):
            st.session_state["prompt_input"] = f"What are the best local street foods and hygiene tips in {dest_city}?"
        if q4.button("🛍️ Bargaining tips?"):
            st.session_state["prompt_input"] = "How do I politely bargain and get the best prices in local bazaars?"

        for msg in st.session_state["copilot_messages"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_query = st.chat_input("Ask a question about this trip...")
        if "prompt_input" in st.session_state and not user_query:
            user_query = st.session_state.pop("prompt_input")

        if user_query:
            st.session_state["copilot_messages"].append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.markdown(user_query)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    context = f"Destination: {dest_city}, {dest_state}. Duration: {days} days. Style: {style}."
                    reply = ask_ai_travel_copilot(user_query, context, api_key=api_key)
                    st.markdown(reply)
                    st.session_state["copilot_messages"].append({"role": "assistant", "content": reply})


# =====================================================================
# VIEW: EXPLORE DESTINATIONS
# =====================================================================
def view_explore(tourist_df):
    st.markdown('<div class="brand-title">🗺️ Explore India\'s 45+ Tourist Destinations</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">Compare baseline rates, best visiting seasons, and highlights across India.</div>', unsafe_allow_html=True)

    ef1, ef2 = st.columns(2)
    zones = ["All Zones"] + sorted(tourist_df["Zone"].unique().tolist())
    selected_zone = ef1.selectbox("Filter by Zone", zones)
    
    categories = ["All Categories"] + sorted(tourist_df["Category"].unique().tolist())
    selected_category = ef2.selectbox("Filter by Category", categories)

    filtered = tourist_df.copy()
    if selected_zone != "All Zones":
        filtered = filtered[filtered["Zone"] == selected_zone]
    if selected_category != "All Categories":
        filtered = filtered[filtered["Category"] == selected_category]

    st.dataframe(
        filtered[[
            "City", "State", "Category", "Best_Months", 
            "Hotel_Budget_Night", "Hotel_Standard_Night", "Key_Attractions"
        ]].rename(columns={
            "Hotel_Budget_Night": "Budget Hotel (₹)",
            "Hotel_Standard_Night": "Standard Hotel (₹)",
            "Best_Months": "Best Season",
            "Key_Attractions": "Highlights"
        }),
        use_container_width=True,
        hide_index=True
    )


# =====================================================================
# VIEW: API SETTINGS (GEMINI & RESEND)
# =====================================================================
def view_settings():
    st.markdown('<div class="brand-title">⚙️ API Settings & Integration</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">Configure your Google Gemini API key and Resend API key for real-time AI and live email OTPs.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🤖 Google Gemini AI")
        st.markdown("Powers real-time dynamic itineraries and personalized travel advice.")
        gemini_input = st.text_input(
            "Gemini API Key",
            value=st.session_state.get("gemini_api_key", ""),
            type="password",
            placeholder="AIzaSy..."
        )
        if st.button("Save Gemini Key", use_container_width=True):
            st.session_state["gemini_api_key"] = gemini_input.strip()
            st.success("✅ Gemini API Key saved for this session!")

    with col2:
        st.markdown("#### 📧 Resend API (Email OTP)")
        st.markdown("Used to deliver 6-digit OTP verification emails for password resets.")
        resend_input = st.text_input(
            "Resend API Key",
            value=st.session_state.get("resend_api_key", ""),
            type="password",
            placeholder="re_..."
        )
        if st.button("Save Resend Key", use_container_width=True):
            st.session_state["resend_api_key"] = resend_input.strip()
            st.success("✅ Resend API Key saved for this session!")

    st.markdown("---")
    st.markdown("##### 💡 How to obtain these keys (100% Free):")
    st.markdown("""
    1. **Google Gemini Key:** Get a free API key at [Google AI Studio](https://aistudio.google.com/).
    2. **Resend Key:** Sign up for free at [Resend.com](https://resend.com/) to send transactional emails via `onboarding@resend.dev`.
    """)


# =====================================================================
# MAIN ROUTING
# =====================================================================
def main():
    init_session_state()
    tourist_df, routes_df = load_datasets()

    # Render sidebar with navigation
    render_sidebar()

    current_page = st.session_state.get("nav_page", "🔐 Sign In")

    # Routing
    if current_page == "🔐 Sign In":
        view_login()
    elif current_page == "📝 Create Account":
        view_signup()
    elif current_page == "🔑 Forgot Password":
        view_forgot_password()
    elif current_page == "📊 Dashboard":
        view_dashboard(tourist_df, routes_df)
    elif current_page in ["🧮 Trip Calculator", "🧮 Guest Trip Calculator"]:
        view_calculator(tourist_df, routes_df)
    elif current_page in ["🌿 AI Travel Studio", "🤖 AI Smart Itinerary", "💬 AI Travel Copilot"]:
        view_ai_studio()
    elif current_page == "🗺️ Explore 45+ Destinations":
        view_explore(tourist_df)
    else:
        view_login()


if __name__ == "__main__":
    main()
