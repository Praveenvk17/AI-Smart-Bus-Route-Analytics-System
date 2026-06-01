# 🚍 AI Smart Bus Route Analytics & Driver Assistance System

## 📌 Project Overview

AI Smart Bus Route Analytics & Driver Assistance System is a machine learning-based web application developed using Streamlit and Random Forest Regression. The system helps private bus operators predict passenger crowd levels, travel delays, traffic risks, fuel efficiency, and route performance.

The project is designed for the **Kallakurichi ↔ Titakudi Private Bus Route** and provides separate dashboards for **Admin** and **Driver** users.

---

## ✨ Features

### 🔐 Login System

* Driver Login
* Admin Login
* Secure role-based access

### 👨‍✈️ Driver Dashboard

Drivers can:

* Enter daily trip details
* Record passenger count
* Record fuel consumption
* Record trip time
* Record delays
* Save data directly into CSV

### 👨‍💼 Admin Dashboard

Admins can:

* Predict passenger crowd using AI
* Predict travel delays
* Analyze fuel consumption
* Monitor route performance
* Download analytics reports

### 🤖 AI Predictions

Machine Learning models predict:

* Expected Passenger Count
* Expected Delay Time

Using:

* Day of Week
* Weather Condition
* Trip Duration

### 🚦 Traffic Risk Prediction

Traffic risk levels:

* 🟢 Low Risk
* 🟡 Medium Risk
* 🔴 High Risk

Based on:

* Predicted Delay
* Weather Conditions

### 📊 Analytics Dashboard

* Monthly Passenger Statistics
* Average Delay Analysis
* Fuel Consumption Analysis
* Peak Crowd Day Detection
* Route Health Score

### 🚨 AI Alerts

Automatic alerts for:

* High Delay
* High Fuel Consumption
* High Passenger Demand
* Route Performance Issues

---

## 🛠️ Technologies Used

* Python
* Streamlit
* Pandas
* Scikit-Learn
* Random Forest Regressor
* CSV Dataset Storage

---

## 📂 Project Structure

```text
AI-Smart-Bus-Analytics/
│
├── app.py                 # Streamlit Web Application
├── main.py                # AI Prediction Console Program
├── data.csv               # Dataset
├── requirements.txt       # Required Libraries
└── README.md
```

---

## 📈 Machine Learning Model

Algorithm Used:

**Random Forest Regressor**

Input Features:

* Day
* Weather
* Trip Time (Minutes)

Output Predictions:

* Passenger Count
* Delay Minutes

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/AI-Smart-Bus-Analytics.git
cd AI-Smart-Bus-Analytics
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Streamlit App

```bash
streamlit run app.py
```

### Run Console Version

```bash
python main.py
```

---

## 🔑 Default Login Credentials

### Driver

Username:

```text
driver
```

Password:

```text
1234
```

### Admin

Username:

```text
admin
```

Password:

```text
admin123
```

---

## 📊 Sample Dataset Columns

```text
date
time
day
weather
passenger_count
fuel_used_liters
trip_time_minutes
delay_minutes
```

---

## 🎯 Future Enhancements

* Real-Time GPS Tracking
* Google Maps Integration
* Live Traffic API
* Fuel Cost Prediction
* Passenger Demand Forecasting
* Cloud Database Integration
* Mobile Application Support
* Advanced AI Models

---

## 👨‍💻 Developed By

aspiring python AI/ML developer

AI Smart Bus Route Analytics & Driver Assistance System

Using Machine Learning and Streamlit
