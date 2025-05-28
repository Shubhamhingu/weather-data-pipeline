# 🌦️ Automated Weather Data Pipeline & Dashboard

A fully automated pipeline that collects weather data from the OpenWeather API, stores it in a SQLite database, and visualizes key trends like temperature and humidity via an interactive dashboard built with **Dash & Plotly**.

---

## 🚀 Features

- 🌐 Fetches real-time weather data for multiple cities using the OpenWeather API
- 🛠️ Transforms and parses weather fields (e.g., temp, humidity, wind, pressure)
- 🗄️ Stores data into a time-series SQLite database with daily scheduled updates
- 📊 Interactive dashboard to explore weather trends by city and time range
- 📅 Historical trend tracking to support decision-making for agriculture/logistics

---

## 🛠 Tech Stack

- **ETL & Automation**: Python, Requests, Pandas, SQLite
- **Dashboard**: Dash, Plotly
- **Scheduler**: PythonAnywhere's task runner (or can be integrated with Airflow/Cron)
- **Data Source**: [OpenWeatherMap API](https://openweathermap.org/api)

---

## 🧱 Project Structure
```
weather-pipeline/
├── data/
│ └── weather.db # SQLite DB storing weather logs
├── scripts/
│ ├── fetch_weather.py # Pulls data from API
│ ├── transform_store.py # Cleans & saves data to DB
├── dashboard/
│ └── app.py # Dash dashboard script
├── utils/
│ └── db_utils.py # Utility functions for DB ops
├── requirements.txt
└── README.md
```

## ✅ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/weather-pipeline.git
   cd weather-pipeline
   ```
Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
Install dependencies

```bash
pip install -r requirements.txt
```
Set up API key

Create a .env file or add your API key in fetch_weather.py:

```txt
API_KEY = "your_openweather_api_key"
```
Run ETL manually

```bash
python scripts/fetch_weather.py
python scripts/transform_store.py
```
Launch Dashboard

```bash

python dashboard/app.py
```
Open browser: http://127.0.0.1:8050/

