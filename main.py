# main.py
from fastapi import FastAPI
from datetime import datetime
import requests
import pandas as pd
import joblib

app = FastAPI()

LAT = "19.0760"
LON = "72.8777"

OWM_API_KEY = "c602c5bd6e4ee77a0c374a852727a1e7"
WAQI_TOKEN = "03a9abaa1a29a978a65f35237a8b0502c434d5e5"

MODEL_PATH = r"models/aqi_model.joblib"
FEATURES = [
    "AQI", "PM2.5", "PM10", "NO2", "SO2", "CO", "O3",
    "temperature_2m", "relative_humidity_2m", "wind_speed_10m"
]

model = joblib.load(MODEL_PATH)

def get_pollutants():
    url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={OWM_API_KEY}"
    res = requests.get(url).json()
    comp = res["list"][0]["components"]
    return {
        "PM2.5": comp["pm2_5"],
        "PM10": comp["pm10"],
        "NO2": comp["no2"],
        "SO2": comp["so2"],
        "CO": comp["co"],
        "O3": comp["o3"]
    }

def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={OWM_API_KEY}&units=metric"
    res = requests.get(url).json()
    return {
        "temperature_2m": res["main"]["temp"],
        "relative_humidity_2m": res["main"]["humidity"],
        "wind_speed_10m": res["wind"]["speed"]
    }

def get_current_aqi():
    url = f"https://api.waqi.info/feed/geo:{LAT};{LON}/?token={WAQI_TOKEN}"
    res = requests.get(url).json()
    return res["data"]["aqi"] if res["status"] == "ok" else None

@app.get("/predict")
def predict():
    try:
        pol_data = get_pollutants()
        weather_data = get_weather()
        current_aqi = get_current_aqi()
        if current_aqi is None:
            raise ValueError("Could not fetch current AQI.")

        full_data = {**pol_data, **weather_data, "AQI": current_aqi}
        df = pd.DataFrame([[full_data[feat] for feat in FEATURES]], columns=FEATURES)
        pred = model.predict(df)[0]

        now = datetime.now()
        today_date = now.strftime("%d %B %Y")
        today_day = now.strftime("%A")

        return {
            "predicted_aqi": float(round(pred, 2)),
            "current_aqi": current_aqi,
            "date": today_date,
            "day": today_day,
            "features": {
                "PM2.5": pol_data["PM2.5"],
                "PM10": pol_data["PM10"],
                "NO2": pol_data["NO2"],
                "SO2": pol_data["SO2"],
                "CO": pol_data["CO"],
                "O3": pol_data["O3"],
                "Humidity": weather_data["relative_humidity_2m"],
                "Wind Speed": weather_data["wind_speed_10m"]
            }
        }

    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def home():
    return {"message": "AQI Prediction FastAPI app running."}
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)