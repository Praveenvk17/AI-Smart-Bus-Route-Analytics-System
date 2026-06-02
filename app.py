import os
from io import BytesIO
from datetime import datetime

import requests
import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="AI Smart Bus Analytics",
    page_icon="🚍",
    layout="wide"
)


# ==================================================
# FILES
# ==================================================
USER_FILE = "users.csv"
LOG_FILE = "driver_logs.csv"


# ==================================================
# DEFAULT USERS
# ==================================================
def create_default_users():
    if not os.path.exists(USER_FILE):
        users = pd.DataFrame(
            [
                {
                    "username": "system_admin",
                    "password": "admin123",
                    "role": "admin"
                },
                {
                    "username": "driver_user",
                    "password": "1234",
                    "role": "driver"
                }
            ]
        )
        users.to_csv(USER_FILE, index=False)


def load_users():
    create_default_users()
    return pd.read_csv(USER_FILE)


def save_users(users):
    users.to_csv(USER_FILE, index=False)


def save_driver_log(username, action):
    log_data = pd.DataFrame(
        [
            {
                "timestamp": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "username": username,
                "action": action
            }
        ]
    )

    if os.path.exists(LOG_FILE):
        old_logs = pd.read_csv(LOG_FILE)
        logs = pd.concat(
            [old_logs, log_data],
            ignore_index=True
        )
    else:
        logs = log_data

    logs.to_csv(LOG_FILE, index=False)


# ==================================================
# PREMIUM RCB STYLE THEME
# ==================================================
st.markdown(
    """
    <style>
    .stApp {
        background: #0d0d0d;
        color: #ffffff;
    }

    h1 {
        color: #D71920;
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        letter-spacing: 1px;
    }

    h2, h3 {
        color: #C9A227;
        font-weight: 700;
    }

    section[data-testid="stSidebar"] {
        background: #141414;
        border-right: 2px solid #D71920;
    }

    .stButton > button {
        background: #D71920;
        color: white;
        border-radius: 12px;
        border: none;
        height: 3em;
        width: 100%;
        font-size: 16px;
        font-weight: bold;
    }

    .stButton > button:hover {
        background: #C9A227;
        color: black;
        transition: 0.3s;
    }

    div[data-testid="metric-container"] {
        background: #1b1b1b;
        border: 1px solid #C9A227;
        border-radius: 16px;
        padding: 16px;
        box-shadow: 0px 0px 10px rgba(215, 25, 32, 0.3);
    }

    .stTextInput input,
    .stNumberInput input,
    .stSelectbox div {
        background-color: #1e1e1e;
        color: white;
        border: 1px solid #444;
        border-radius: 10px;
    }

    section[data-testid="stFileUploader"] {
        border: 2px dashed #D71920;
        border-radius: 12px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# CENTER LOGIN SYSTEM
# ==================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = ""
    st.session_state.username = ""

if not st.session_state.logged_in:

    st.markdown(
        """
        <h1 style='text-align:center;color:#D71920;'>
        🚍 AI Smart Bus Route Analytics
        </h1>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("## 🔐 Secure Login")
        st.info(
            "Authorized users only. Please enter your credentials."
        )

        username = st.text_input("Username")
        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):
            users = load_users()

            matched_user = users[
                (users["username"] == username)
                & (users["password"] == password)
            ]

            if len(matched_user) > 0:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.user_role = (
                    matched_user.iloc[0]["role"]
                )

                st.success("✅ Login successful")
                st.rerun()

            else:
                st.error("❌ Invalid username or password")

    st.stop()

user_role = st.session_state.user_role
logged_username = st.session_state.username


# ==================================================
# LOGOUT BUTTON
# ==================================================
st.sidebar.success(
    f"Logged in as: {logged_username}"
)

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.user_role = ""
    st.session_state.username = ""
    st.rerun()


# ==================================================
# PAGE TITLE
# ==================================================
st.title(
    "🚍 AI Smart Bus Route Analytics & Driver Assistance System"
)

st.write(
    "AI-powered system to predict passenger crowd, delay, fuel usage, traffic risk, and route health."
)

st.write(
    "Kallakurichi ↔ Titakudi Private Bus AI Assistant"
)


# ==================================================
# LOAD CSV
# ==================================================
uploaded_file = st.file_uploader(
    "📂 Upload Bus Data CSV File",
    type=["csv"]
)

try:
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.success("✅ Uploaded CSV Loaded Successfully")
    else:
        data = pd.read_csv("data.csv")

except Exception as e:
    st.error(f"❌ Error loading CSV: {e}")
    st.stop()


required_columns = [
    "date",
    "time",
    "day",
    "weather",
    "passenger_count",
    "fuel_used_liters",
    "trip_time_minutes",
    "delay_minutes"
]

missing_columns = [
    col for col in required_columns
    if col not in data.columns
]

if missing_columns:
    st.error(
        f"❌ Missing columns in CSV: {missing_columns}"
    )
    st.stop()


# ==================================================
# DAY & WEATHER MAPPING
# ==================================================
day_mapping = {
    "Monday": 1,
    "Tuesday": 2,
    "Wednesday": 3,
    "Thursday": 4,
    "Friday": 5,
    "Saturday": 6,
    "Sunday": 7
}

weather_mapping = {
    "Sunny": 1,
    "Cloudy": 2,
    "Rainy": 3
}

day_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]


# ==================================================
# PREPARE DATA
# ==================================================
data["day"] = (
    data["day"]
    .astype(str)
    .str.strip()
    .str.title()
)

data["weather"] = (
    data["weather"]
    .astype(str)
    .str.strip()
    .str.title()
)

model_data = data.copy()

model_data["day"] = model_data["day"].map(
    day_mapping
)

model_data["weather"] = model_data["weather"].map(
    weather_mapping
)

model_data = model_data.dropna(
    subset=["day", "weather"]
)

if len(model_data) == 0:
    st.error("❌ No valid data found.")
    st.stop()


# ==================================================
# TRAIN MODELS
# ==================================================
X = model_data[
    ["day", "weather", "trip_time_minutes"]
]

y = model_data["passenger_count"]

passenger_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

passenger_model.fit(X, y)


X_delay = model_data[
    ["day", "weather", "trip_time_minutes"]
]

y_delay = model_data["delay_minutes"]

delay_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

delay_model.fit(X_delay, y_delay)


# ==================================================
# LIVE WEATHER API
# ==================================================
def get_live_weather():
    try:
        # Kallakurichi approximate coordinates
        latitude = 11.7404
        longitude = 78.9597

        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}"
            f"&longitude={longitude}"
            "&current_weather=true"
        )

        response = requests.get(
            url,
            timeout=10
        )

        result = response.json()
        weather_data = result.get(
            "current_weather",
            {}
        )

        temperature = weather_data.get(
            "temperature",
            "N/A"
        )

        windspeed = weather_data.get(
            "windspeed",
            "N/A"
        )

        return temperature, windspeed

    except Exception:
        return "N/A", "N/A"


# ==================================================
# PDF REPORT FUNCTION
# ==================================================
def generate_pdf_report(
    total_passengers,
    avg_delay,
    avg_fuel,
    highest_day,
    health_score,
    health_status
):
    buffer = BytesIO()

    pdf = canvas.Canvas(
        buffer,
        pagesize=letter
    )

    pdf.setFont(
        "Helvetica-Bold",
        16
    )

    pdf.drawString(
        50,
        750,
        "AI Smart Bus Route Analytics Report"
    )

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.drawString(
        50,
        720,
        "Route: Kallakurichi to Titakudi"
    )

    pdf.drawString(
        50,
        690,
        f"Total Passengers: {total_passengers}"
    )

    pdf.drawString(
        50,
        670,
        f"Average Delay: {avg_delay} minutes"
    )

    pdf.drawString(
        50,
        650,
        f"Average Fuel Usage: {avg_fuel} liters"
    )

    pdf.drawString(
        50,
        630,
        f"Peak Crowd Day: {highest_day}"
    )

    pdf.drawString(
        50,
        610,
        f"Route Health Score: {health_score}/100"
    )

    pdf.drawString(
        50,
        590,
        f"Health Status: {health_status}"
    )

    pdf.drawString(
        50,
        550,
        "Generated by AI Smart Bus Route Analytics System"
    )

    pdf.save()
    buffer.seek(0)

    return buffer


# ==================================================
# ADMIN ACCESS
# ==================================================
if user_role == "admin":

    st.subheader("🚌 Enter Trip Details for Analytics")

    col1, col2 = st.columns(2)

    with col1:
        day = st.selectbox(
            "Select Day",
            list(day_mapping.keys())
        )

        weather = st.selectbox(
            "Select Weather",
            list(weather_mapping.keys())
        )

    with col2:
        trip_time = st.number_input(
            "Trip Time (minutes)",
            min_value=1,
            value=60
        )

        fuel_used = st.number_input(
            "Fuel Used (liters)",
            min_value=1.0,
            value=8.0
        )

    if st.button("🚍 Predict Bus Analytics"):

        day_num = day_mapping[day]
        weather_num = weather_mapping[weather]

        prediction = passenger_model.predict(
            [[day_num, weather_num, trip_time]]
        )

        predicted_passengers = round(
            prediction[0]
        )

        delay_prediction = delay_model.predict(
            [[day_num, weather_num, trip_time]]
        )

        predicted_delay = round(
            delay_prediction[0]
        )

        st.success(
            f"👥 Expected Passengers: {predicted_passengers}"
        )

        st.info(
            f"⏰ Expected Delay: {predicted_delay} mins"
        )

        st.subheader("🤖 AI Smart Suggestions")

        if predicted_passengers > 50:
            st.warning(
                "🚍 High crowd expected. Consider extra trip."
            )
        elif predicted_passengers > 30:
            st.info(
                "🟡 Moderate crowd expected."
            )
        else:
            st.success(
                "🟢 Low crowd expected."
            )

        if predicted_delay > 15:
            st.warning(
                "⏰ High delay expected. Start earlier."
            )
        elif predicted_delay > 5:
            st.info(
                "🟡 Moderate delay possible."
            )
        else:
            st.success(
                "✅ Trip likely on time."
            )

        if fuel_used > 9:
            st.warning(
                "⛽ Fuel usage high. Maintenance recommended."
            )
        elif fuel_used > 7:
            st.info(
                "🟡 Fuel usage normal."
            )
        else:
            st.success(
                "✅ Fuel efficient."
            )

        st.subheader("🚦 Traffic Risk Prediction")

        if predicted_delay > 15 or weather == "Rainy":
            st.error("🔴 High Traffic Risk")
        elif predicted_delay > 5:
            st.warning("🟡 Medium Traffic Risk")
        else:
            st.success("🟢 Low Traffic Risk")

    # ==================================================
    # LIVE WEATHER
    # ==================================================
    st.subheader("🌦️ Live Weather Update")

    temperature, windspeed = get_live_weather()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "🌡️ Temperature",
            f"{temperature} °C"
        )

    with col2:
        st.metric(
            "💨 Wind Speed",
            f"{windspeed} km/h"
        )

    # ==================================================
    # GOOGLE MAPS ROUTE VISUALIZATION
    # ==================================================
    st.subheader("🗺️ Route Map: Kallakurichi → Titakudi")

    google_map_html = """
    <iframe
        width="100%"
        height="420"
        style="border:0; border-radius:15px;"
        loading="lazy"
        allowfullscreen
        src="https://www.google.com/maps?q=Kallakurichi%20to%20Titakudi&output=embed">
    </iframe>
    """

    st.markdown(
        google_map_html,
        unsafe_allow_html=True
    )

    # ==================================================
    # PASSENGER ANALYTICS
    # ==================================================
    st.subheader("📊 Passenger Analytics")

    avg_passengers = (
        data.groupby("day")[
            "passenger_count"
        ]
        .mean()
        .reindex(day_order)
    )

    st.bar_chart(avg_passengers)

    # ==================================================
    # MONTHLY ANALYTICS DASHBOARD
    # ==================================================
    st.subheader("📈 Monthly Analytics Dashboard")

    total_passengers = int(
        data["passenger_count"].sum()
    )

    avg_delay = round(
        data["delay_minutes"].mean(),
        2
    )

    avg_fuel = round(
        data["fuel_used_liters"].mean(),
        2
    )

    highest_day = (
        data.groupby("day")[
            "passenger_count"
        ]
        .mean()
        .idxmax()
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "👥 Total Passengers",
            total_passengers
        )

        st.metric(
            "⛽ Avg Fuel Usage",
            f"{avg_fuel} L"
        )

    with col2:
        st.metric(
            "⏰ Avg Delay",
            f"{avg_delay} mins"
        )

        st.metric(
            "🔥 Peak Crowd Day",
            highest_day
        )

    # ==================================================
    # DELAY ANALYTICS
    # ==================================================
    st.subheader("⏰ Average Delay by Day")

    delay_chart = (
        data.groupby("day")[
            "delay_minutes"
        ]
        .mean()
        .reindex(day_order)
    )

    st.line_chart(delay_chart)

    # ==================================================
    # FUEL ANALYTICS
    # ==================================================
    st.subheader("⛽ Fuel Usage Analytics")

    fuel_chart = (
        data.groupby("day")[
            "fuel_used_liters"
        ]
        .mean()
        .reindex(day_order)
    )

    st.bar_chart(fuel_chart)

    # ==================================================
    # AI BUS HEALTH & ALERTS
    # ==================================================
    st.subheader("🚨 AI Bus Health & Alerts")

    health_score = 100

    if avg_delay > 15:
        health_score -= 25
    elif avg_delay > 5:
        health_score -= 10

    if avg_fuel > 10:
        health_score -= 25
    elif avg_fuel > 7:
        health_score -= 10

    if total_passengers < 50:
        health_score -= 15

    if health_score >= 80:
        health_status = "🟢 Good"
    elif health_score >= 60:
        health_status = "🟡 Moderate"
    else:
        health_status = "🔴 Needs Attention"

    st.metric(
        "🚍 Route Health Score",
        f"{health_score}/100"
    )

    st.write(
        f"Status: {health_status}"
    )

    st.subheader("🤖 AI Alerts")

    if avg_delay > 10:
        st.warning(
            "⏰ Average delay is high. Consider starting earlier."
        )

    if avg_fuel > 9:
        st.warning(
            "⛽ Fuel consumption is high. Vehicle maintenance recommended."
        )

    if total_passengers > 300:
        st.info(
            "🚍 High passenger demand detected. Consider extra trips."
        )

    if total_passengers < 100:
        st.success(
            "🟢 Passenger crowd normal."
        )

    # ==================================================
    # DOWNLOAD REPORTS
    # ==================================================
    st.subheader("📥 Download Analytics Reports")

    csv = data.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📂 Download CSV Report",
        data=csv,
        file_name="bus_analytics_report.csv",
        mime="text/csv"
    )

    pdf_report = generate_pdf_report(
        total_passengers,
        avg_delay,
        avg_fuel,
        highest_day,
        health_score,
        health_status
    )

    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_report,
        file_name="bus_analytics_report.pdf",
        mime="application/pdf"
    )

    # ==================================================
    # ADMIN PASSWORD CHANGE
    # ==================================================
    st.subheader("🔐 Admin Password Change")

    with st.expander("Change Admin Password"):
        old_password = st.text_input(
            "Current Password",
            type="password"
        )

        new_password = st.text_input(
            "New Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm New Password",
            type="password"
        )

        if st.button("Update Password"):
            users = load_users()

            current_user = users[
                users["username"] == logged_username
            ]

            if len(current_user) == 0:
                st.error("❌ User not found")

            elif (
                current_user.iloc[0]["password"]
                != old_password
            ):
                st.error("❌ Current password is wrong")

            elif new_password != confirm_password:
                st.error("❌ Passwords do not match")

            elif len(new_password) < 4:
                st.warning(
                    "⚠️ Password must be at least 4 characters"
                )

            else:
                users.loc[
                    users["username"] == logged_username,
                    "password"
                ] = new_password

                save_users(users)

                st.success(
                    "✅ Password updated successfully. Please logout and login again."
                )

    # ==================================================
    # DRIVER ACTIVITY LOGS
    # ==================================================
    st.subheader("📋 Driver Activity Logs")

    if os.path.exists(LOG_FILE):
        logs = pd.read_csv(LOG_FILE)
        st.dataframe(
            logs.tail(20),
            use_container_width=True
        )
    else:
        st.info("No driver activity logs found yet.")


# ==================================================
# DRIVER ACCESS
# ==================================================
elif user_role == "driver":

    st.subheader("👨‍✈️ Driver Dashboard")

    st.info(
        "Driver can only enter daily data."
    )

    entry_date = st.date_input("Date")
    entry_time = st.text_input("Time")

    entry_day = st.selectbox(
        "Day",
        list(day_mapping.keys())
    )

    entry_weather = st.selectbox(
        "Weather",
        list(weather_mapping.keys())
    )

    entry_passengers = st.number_input(
        "Passenger Count",
        min_value=0,
        value=30
    )

    entry_fuel = st.number_input(
        "Fuel Used",
        min_value=0.0,
        value=8.0
    )

    entry_trip_time = st.number_input(
        "Trip Time",
        min_value=1,
        value=60
    )

    entry_delay = st.number_input(
        "Delay",
        min_value=0,
        value=0
    )

    if st.button("💾 Save Daily Data"):

        new_entry = {
            "date": str(entry_date),
            "time": entry_time,
            "day": entry_day,
            "weather": entry_weather,
            "passenger_count": entry_passengers,
            "fuel_used_liters": entry_fuel,
            "trip_time_minutes": entry_trip_time,
            "delay_minutes": entry_delay
        }

        updated_data = pd.concat(
            [
                data,
                pd.DataFrame([new_entry])
            ],
            ignore_index=True
        )

        updated_data.to_csv(
            "data.csv",
            index=False
        )

        save_driver_log(
            logged_username,
            "Daily bus data saved"
        )

        st.success(
            "✅ Data Saved Successfully!"
        )
