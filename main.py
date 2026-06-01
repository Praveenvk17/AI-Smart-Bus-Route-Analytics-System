import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Load dataset
data = pd.read_csv("data.csv")

# Convert text into numbers
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

# Convert dataset text to numbers
data["day"] = data["day"].map(day_mapping)
data["weather"] = data["weather"].map(weather_mapping)

# Input features
X = data[["day", "weather", "trip_time_minutes"]]

# Output target
y = data["passenger_count"]

# Train model
model = RandomForestRegressor()
model.fit(X, y)

print("===== AI Bus Passenger Prediction =====")

# User Input
day = input("Enter day (Monday-Sunday): ")
weather = input("Enter weather (Sunny/Cloudy/Rainy): ")
trip_time = int(input("Enter trip time in minutes: "))

# Convert input into numbers
day_num = day_mapping[day]
weather_num = weather_mapping[weather]

# Prediction
prediction = model.predict([[day_num, weather_num, trip_time]])

print("\nExpected Passenger Count:", round(prediction[0]))
predicted_passengers = round(prediction[0])

if predicted_passengers > 50:
    print("High Crowd Expected - Extra Attention Needed")
elif predicted_passengers > 30:
    print("Medium Crowd Expected")
else:
    print("Low Crowd Expected")