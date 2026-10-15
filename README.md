# 🇮🇳 Bharat Yatra: India Tourist Cities Travel Cost Calculator & AI Planner

A complete domestic Indian travel web platform featuring **User Authentication**, a personal **Travel Dashboard**, **Trip Cost Calculator** in Indian Rupee (**₹ INR**), **AI Day-by-Day Itineraries**, and **YatraAI: 24/7 AI Travel Copilot**.

---

## 🌟 Key Platform Features

1. **🔐 Authentication & User Accounts**:
   - **Sign Up**: Create an account with full name, email, and secure hashed password.
   - **Sign In**: Log into your personal account (or use the 1-Click Demo Account: `demo@yatra.com` / `demo123`).
   - **Forgot Password with OTP**: 6-digit OTP verification delivered directly to your email via the **Resend API**.

2. **📊 Personal User Dashboard**:
   - Track planned trips and total estimated travel budget.
   - Save estimated trips with one click from the calculator.
   - View, review, or delete trip estimates anytime.

3. **🧮 45+ Indian Destinations Budget Calculator**:
   - Accurate baseline rates for 45+ tourist cities across all zones in India.
   - **Inter-city Transit**: Flights, Trains (3AC / Vande Bharat / Sleeper), AC Volvo Buses, or Personal Drive with automatic fare estimation.
   - **Customizable Daily Rates**: Auto-fills realistic rates for Budget, Standard, and Luxury tiers with an optional fine-tuning expander.
   - **Visual Breakdown**: Interactive bar chart and itemized table with exportable WhatsApp/Email summary.

4. **🤖 Dual-Engine AI Integration**:
   - **Google Gemini Generative AI**: Connect your free Gemini API key in Settings for live dynamic itineraries and deep travel advice.
   - **Built-in Smart Offline AI**: If no API key is set, the app seamlessly uses a built-in intelligent engine with local tourist attraction databases, food recommendations, and budget-saving hacks—**100% free with zero configuration**.

5. **💬 24/7 YatraAI Travel Copilot (Chatbot)**:
   - Ask travel questions anytime: packing checklists, safety for solo travelers, local street food hygiene, and market bargaining hacks.

---

## 📂 Project Architecture

```text
travel_cost_calculator/
├── .streamlit/
│   └── config.toml                # Modern UI theme & server settings
├── data/
│   ├── india_tourist_cities.csv   # Comprehensive database of 45+ Indian tourist cities
│   └── india_routes.csv           # Indicative inter-city transport fares and distances
├── src/
│   ├── app.py                     # Main application platform (Dashboard, Auth, Calculator)
│   ├── auth.py                    # SQLite database, user accounts, and Resend OTP delivery
│   ├── travel_calculator.py       # Core budget calculation engine & INR formatting
│   ├── ai_planner.py              # AI itinerary generator & YatraAI travel copilot
│   └── data.py                    # Constants, hubs, states, and travel styles
├── tests/
│   └── test_calculator.py         # Automated unit tests (pytest)
├── app.py                         # Root entrypoint wrapper
├── Dockerfile                     # Production container image setup
├── .dockerignore
├── requirements.txt               # Dependencies (streamlit, pandas, google-genai, resend, pytest)
└── README.md                      # Documentation & deployment guide
```

---

## 🚀 How to Run Locally

Run the app using Python 3.14:

```powershell
# 1. Install dependencies (resend, streamlit, pandas, google-genai)
python -m pip install -r requirements.txt

# 2. Launch the Web Platform
python -m streamlit run app.py
```
*The app will automatically open in your default browser at `http://localhost:8501`.*

---

## 🔑 Adding API Keys (Gemini & Resend)

You can provide API keys directly inside the app:
1. Navigate to **⚙️ API Settings** in the sidebar.
2. Enter your **Google Gemini API Key** (from [Google AI Studio](https://aistudio.google.com/)).
3. Enter your **Resend API Key** (from [Resend.com](https://resend.com/)).
4. Click **Save**!

> **Note:** If no keys are entered, the app still works! It uses the built-in smart AI fallback for itineraries, and shows a test code for password reset OTPs.

---

## 🌐 How to Deploy (Step-by-Step on Streamlit Cloud)

1. **Push your code to your GitHub repo**:
   ```bash
   git add .
   git commit -m "feat: complete web dashboard with auth, resend otp, and ai travel planner"
   git push origin main
   ```
2. Go to **[share.streamlit.io](https://share.streamlit.io/)** and sign in with GitHub.
3. Click **"New app"** -> select your repo -> set file path to `app.py`.
4. Under **Advanced settings -> Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your-gemini-key"
   RESEND_API_KEY = "your-resend-key"
   ```
5. Click **Deploy!** Your full web platform is live in under 2 minutes.
