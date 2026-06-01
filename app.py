import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# ==================================================
# CENTER LOGIN SYSTEM
# ==================================================
USER_CREDENTIALS = {
    "driver": "1234",
    "admin": "admin123"
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = ""

if not st.session_state.logged_in:

    st.markdown(
        """
        <h1 style='text-align:center;
        color:#D71920;'>
        🚍 AI Smart Bus Route Analytics
        </h1>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.markdown("## 🔐 Login")

        st.info("""
👤 Driver Login  
Username: driver  
Password: 1234

👤 Admin Login  
Username: admin  
Password: admin123
""")

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            if (
                username in USER_CREDENTIALS
                and USER_CREDENTIALS[
                    username
                ] == password
            ):

                st.session_state.logged_in = True
                st.session_state.user_role = username

                st.success(
                    f"✅ Welcome {username}"
                )

                st.rerun()

            else:
                st.error(
                    "❌ Invalid Login"
                )

    st.stop()

user_role = st.session_state.user_role

# ==================================================
# LOGOUT BUTTON
# ==================================================
if st.sidebar.button("🚪 Logout"):

    st.session_state.logged_in = False
    st.session_state.user_role = ""

    st.rerun()

# ==================================================
# PREMIUM RCB STYLE THEME
# ==================================================
st.markdown(
    """
    <style>

    /* Main Background */
    .stApp {
        background: #0d0d0d;
        color: #ffffff;
    }

    /* Title */
    h1 {
        color: #D71920;
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        letter-spacing: 1px;
    }

    /* Headings */
    h2, h3 {
        color: #C9A227;
        font-weight: 700;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #141414;
        border-right: 2px solid #D71920;
    }

    /* Buttons */
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

    /* Metric Cards */
    div[data-testid="metric-container"] {
        background: #1b1b1b;
        border: 1px solid #C9A227;
        border-radius: 16px;
        padding: 16px;
        box-shadow: 0px 0px 10px rgba(
            215, 25, 32, 0.3
        );
    }

    /* Input Boxes */
    .stTextInput input,
    .stNumberInput input,
    .stSelectbox div {
        background-color: #1e1e1e;
        color: white;
        border: 1px solid #444;
        border-radius: 10px;
    }

    /* Upload Box */
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
# PAGE TITLE
# ==================================================
st.title(
    "🚍 AI Smart Bus Route Analytics & Driver Assistance System"
)

st.write(
    "AI-powered system to predict passenger crowd and travel delay"
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
        st.success(
            "✅ Uploaded CSV Loaded Successfully"
        )
    else:
        data = pd.read_csv(
            "data.csv"
        )

except Exception as e:
    st.error(
        f"❌ Error loading CSV: {e}"
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

# ==================================================
# PREPARE DATA FOR ML
# ==================================================
model_data = data.copy()

model_data["day"] = (
    model_data["day"]
    .astype(str)
    .str.strip()
    .str.title()
)

model_data["weather"] = (
    model_data["weather"]
    .astype(str)
    .str.strip()
    .str.title()
)

model_data["day"] = (
    model_data["day"]
    .map(day_mapping)
)

model_data["weather"] = (
    model_data["weather"]
    .map(weather_mapping)
)

model_data = model_data.dropna(
    subset=["day", "weather"]
)

if len(model_data) == 0:
    st.error(
        "❌ No valid data found."
    )
    st.stop()

# ==================================================
# TRAIN MODEL
# ==================================================
X = model_data[
    [
        "day",
        "weather",
        "trip_time_minutes"
    ]
]

y = model_data[
    "passenger_count"
]

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

X_delay = model_data[
    [
        "day",
        "weather",
        "trip_time_minutes"
    ]
]

y_delay = model_data[
    "delay_minutes"
]

delay_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

delay_model.fit(
    X_delay,
    y_delay
)

# ==================================================
# ADMIN ACCESS
# ==================================================
if user_role == "admin":

    st.subheader(
        "🚌 Enter Trip Details"
    )

    day = st.selectbox(
        "Select Day",
        list(day_mapping.keys())
    )

    weather = st.selectbox(
        "Select Weather",
        list(weather_mapping.keys())
    )

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

    if st.button(
        "🚍 Predict Bus Analytics"
    ):

        day_num = day_mapping[day]
        weather_num = weather_mapping[
            weather
        ]

        prediction = model.predict(
            [[
                day_num,
                weather_num,
                trip_time
            ]]
        )

        predicted_passengers = round(
            prediction[0]
        )

        delay_prediction = (
            delay_model.predict(
                [[
                    day_num,
                    weather_num,
                    trip_time
                ]]
            )
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

        # AI Suggestions
        st.subheader(
            "🤖 AI Smart Suggestions"
        )

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
        # ==================================================
        # TRAFFIC RISK PREDICTION
        # ==================================================
        st.subheader(
            "🚦 Traffic Risk Prediction"
        )

        if (
            predicted_delay > 15
            or weather == "Rainy"
        ):
            st.error(
                "🔴 High Traffic Risk"
            )

        elif predicted_delay > 5:
            st.warning(
                "🟡 Medium Traffic Risk"
            )

        else:
            st.success(
                "🟢 Low Traffic Risk"
            )

        # ==================================================
        # DOWNLOAD ANALYTICS REPORT
        # ==================================================
        st.subheader(
            "📥 Download Analytics Report"
        )

        csv = data.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📂 Download Report CSV",
            data=csv,
            file_name=
            "bus_analytics_report.csv",
            mime="text/csv"
        )
        # Analytics
        st.subheader(
            "📊 Passenger Analytics"
        )

        avg_passengers = (
            data.groupby("day")[
                "passenger_count"
            ]
            .mean()
        )

        st.bar_chart(
            avg_passengers
        )
        # ==================================================
    # MONTHLY ANALYTICS DASHBOARD
    # ==================================================
    st.subheader(
        "📈 Monthly Analytics Dashboard"
    )

    # Total Passengers
    total_passengers = data[
        "passenger_count"
    ].sum()

    # Average Delay
    avg_delay = round(
        data["delay_minutes"].mean(),
        2
    )

    # Average Fuel Usage
    avg_fuel = round(
        data[
            "fuel_used_liters"
        ].mean(),
        2
    )

    # Highest Crowd Day
    highest_day = (
        data.groupby("day")[
            "passenger_count"
        ]
        .mean()
        .idxmax()
    )

    # Dashboard Metrics
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
    st.subheader(
        "⏰ Average Delay by Day"
    )

    delay_chart = (
        data.groupby("day")[
            "delay_minutes"
        ]
        .mean()
    )

    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    delay_chart = (
        delay_chart.reindex(
            day_order
        )
    )

    st.line_chart(
        delay_chart
    )

    # ==================================================
    # FUEL ANALYTICS
    # ==================================================
    st.subheader(
        "⛽ Fuel Usage Analytics"
    )

    fuel_chart = (
        data.groupby("day")[
            "fuel_used_liters"
        ]
        .mean()
    )

    fuel_chart = (
        fuel_chart.reindex(
            day_order
        )
    )

    st.bar_chart(
        fuel_chart
    )

    # ==================================================
    # AI BUS HEALTH & ALERTS
    # ==================================================
    st.subheader(
        "🚨 AI Bus Health & Alerts"
    )

    health_score = 100

    if avg_delay > 10:
        health_score -= 20

    if avg_fuel > 9:
        health_score -= 20

    if total_passengers < 30:
        health_score -= 10

    # Health Status
    if health_score >= 80:
        health_status = "🟢 Good"

    elif health_score >= 60:
        health_status = "🟡 Moderate"

    else:
        health_status = (
            "🔴 Needs Attention"
        )

    st.metric(
        "🚍 Route Health Score",
        f"{health_score}/100"
    )

    st.write(
        f"Status: {health_status}"
    )

    # ==================================================
    # AI ALERTS
    # ==================================================
    st.subheader(
        "🤖 AI Alerts"
    )

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
# DRIVER ACCESS
# ==================================================
elif user_role == "driver":

    st.subheader(
        "👨‍✈️ Driver Dashboard"
    )

    st.info(
        "Driver can only enter daily data."
    )

    entry_date = st.date_input(
        "Date"
    )

    entry_time = st.text_input(
        "Time"
    )

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

    if st.button(
        "💾 Save Daily Data"
    ):

        new_entry = {
            "date": str(entry_date),
            "time": entry_time,
            "day": entry_day,
            "weather": entry_weather,
            "passenger_count":
                entry_passengers,
            "fuel_used_liters":
                entry_fuel,
            "trip_time_minutes":
                entry_trip_time,
            "delay_minutes":
                entry_delay
        }

        updated_data = pd.concat(
            [
                data,
                pd.DataFrame(
                    [new_entry]
                )
            ],
            ignore_index=True
        )

        updated_data.to_csv(
            "data.csv",
            index=False
        )

        st.success(
            "✅ Data Saved Successfully!"
        )
