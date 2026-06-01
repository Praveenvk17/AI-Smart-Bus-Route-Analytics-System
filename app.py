import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# -------------------------
# Page Title
# -------------------------
st.title("🚍 AI Smart Bus Route Analytics & Driver Assistance System")

st.write(
    "AI-powered system to predict passenger crowd and travel delay for private bus operations"
)

st.write("Kallakurichi ↔ Titakudi Private Bus AI Assistant")

# -------------------------
# Load Dataset
# -------------------------
data = pd.read_csv("data.csv")

# -------------------------
# Convert Text to Numbers
# -------------------------
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

# Convert dataset values
data["day"] = data["day"].map(day_mapping)
data["weather"] = data["weather"].map(weather_mapping)

# -------------------------
# Passenger Prediction Model
# -------------------------
X = data[["day", "weather", "trip_time_minutes"]]
y = data["passenger_count"]

model = RandomForestRegressor()
model.fit(X, y)

# -------------------------
# Delay Prediction Model
# -------------------------
X_delay = data[["day", "weather", "trip_time_minutes"]]
y_delay = data["delay_minutes"]

delay_model = RandomForestRegressor()
delay_model.fit(X_delay, y_delay)

# -------------------------
# User Input
# -------------------------
st.subheader("Enter Trip Details")

day = st.selectbox(
    "Select Day",
    [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]
)

weather = st.selectbox(
    "Select Weather",
    ["Sunny", "Cloudy", "Rainy"]
)

trip_time = st.number_input(
    "Enter Trip Time (minutes)",
    min_value=1,
    value=60
)

fuel_used = st.number_input(
    "Enter Fuel Used (liters)",
    min_value=1.0,
    value=8.0
)

# -------------------------
# Prediction Button
# -------------------------
if st.button("Predict Bus Analytics"):

    day_num = day_mapping[day]
    weather_num = weather_mapping[weather]

    # Passenger Prediction
    prediction = model.predict(
        [[day_num, weather_num, trip_time]]
    )

    predicted_passengers = round(prediction[0])

    # Delay Prediction
    delay_prediction = delay_model.predict(
        [[day_num, weather_num, trip_time]]
    )

    predicted_delay = round(delay_prediction[0])

    # Fuel Efficiency Check
    if fuel_used > 9:
        fuel_status = "⚠️ High Fuel Consumption"
    elif fuel_used > 7:
        fuel_status = "🟡 Normal Fuel Usage"
    else:
        fuel_status = "🟢 Fuel Efficient"

    # Results
    st.subheader("📌 Prediction Results")

    st.success(
        f"Expected Passenger Count: {predicted_passengers}"
    )

    st.info(
        f"Expected Delay: {predicted_delay} minutes"
    )

    st.write(f"Fuel Status: {fuel_status}")

    # Crowd Level
    if predicted_passengers > 50:
        st.warning("⚠️ High Crowd Expected")
    elif predicted_passengers > 30:
        st.info("🟡 Medium Crowd Expected")
    else:
        st.success("🟢 Low Crowd Expected")

# -------------------------
# Analytics Graph
# -------------------------
st.subheader("📊 Passenger Analytics")

st.write("Average passenger crowd across weekdays")

day_names = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
    7: "Sunday"
}

graph_data = data.copy()
graph_data["day"] = graph_data["day"].map(day_names)

avg_passengers = graph_data.groupby(
    "day"
)["passenger_count"].mean()

st.bar_chart(avg_passengers)