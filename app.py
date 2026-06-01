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
# CSV Upload Option
# -------------------------
uploaded_file = st.file_uploader(
    "📂 Upload Bus Data CSV File",
    type=["csv"]
)

# -------------------------
# Load Dataset
# -------------------------
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.success("✅ Uploaded CSV Loaded Successfully")
else:
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
# -------------------------
# Daily Data Entry Form
# -------------------------
st.subheader("📝 Daily Bus Data Entry")

entry_date = st.date_input("Date")

entry_time = st.text_input(
    "Time (Example: 07:30)"
)

entry_day = st.selectbox(
    "Day for Entry",
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

entry_weather = st.selectbox(
    "Weather for Entry",
    ["Sunny", "Cloudy", "Rainy"]
)

entry_passengers = st.number_input(
    "Passenger Count",
    min_value=0,
    value=30
)

entry_fuel = st.number_input(
    "Fuel Used (Liters)",
    min_value=0.0,
    value=8.0
)

entry_trip_time = st.number_input(
    "Trip Time (Minutes)",
    min_value=1,
    value=60
)

entry_delay = st.number_input(
    "Delay (Minutes)",
    min_value=0,
    value=0
)

# Save Button
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

    # Add new row
    new_data = pd.DataFrame([new_entry])

    updated_data = pd.concat(
        [data, new_data],
        ignore_index=True
    )

    # Save to CSV
    updated_data.to_csv(
        "data.csv",
        index=False
    )

    st.success(
        "✅ Daily Bus Data Saved Successfully!"
    )
