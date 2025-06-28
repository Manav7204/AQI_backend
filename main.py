# main.py
from fastapi import FastAPI
import requests
import pandas as pd
import joblib
import os

# Initialize FastAPI app
app = FastAPI()

# ------------------ CONFIGURATION ------------------
# Latitude and Longitude for Mumbai (change if needed)
LAT = "19.0760"
LON = "72.8777"

# ------------------ API KEYS ------------------
# You must set your API keys below.
# These are required to authenticate your requests to the external APIs.
# Get your OpenWeatherMap API key from: https://home.openweathermap.org/api_keys
# Get your WAQI token from: https://aqicn.org/data-platform/token/

OWM_API_KEY = "c602c5bd6e4ee77a0c374a852727a1e7"  # Put your key here if not using env vars
WAQI_TOKEN = "03a9abaa1a29a978a65f35237a8b0502c434d5e5"           # Put your token here if not using env vars

# OR optionally: use environment variables and set them securely
# Example (in terminal): export OWM_API_KEY="your_actual_key"

# Path to the trained XGBoost model saved using joblib
MODEL_PATH = "model.joblib"

# Features that the model expects (ensure this order matches training phase)
FEATURES = [
    "AQI", "PM2.5", "PM10", "NO2", "SO2", "CO", "O3",
    "temperature_2m", "relative_humidity_2m", "wind_speed_10m"
]

# ------------------ LOAD MODEL ------------------
# Load the trained ML model (.joblib format). Make sure this file exists.
model = joblib.load(r"C:\Users\manav\Desktop\AQI Prediction\models\aqi_model.joblib")

# ------------------ FETCH POLLUTANT DATA ------------------
def get_pollutants():
    """
    Calls OpenWeatherMap's Air Pollution API to retrieve pollutant concentrations.
    Returns a dictionary with pollutant levels in μg/m³.
    """
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

# ------------------ FETCH WEATHER DATA ------------------
def get_weather():
    """
    Fetch temperature, humidity, and wind speed using OpenWeatherMap's Current Weather API.
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={OWM_API_KEY}&units=metric"
    res = requests.get(url).json()

    try:
        return {
            "temperature_2m": res["main"]["temp"],
            "relative_humidity_2m": res["main"]["humidity"],
            "wind_speed_10m": res["wind"]["speed"]
        }
    except KeyError as e:
        raise ValueError(f"Missing key in weather response: {e}, full response: {res}")



# ------------------ FETCH CURRENT AQI ------------------
def get_current_aqi():
    """
    Fetches the current AQI (Air Quality Index) value using WAQI API.
    This is OPTIONAL and only for reference (not used in prediction).
    """
    try:
        url = f"https://api.waqi.info/feed/geo:{LAT};{LON}/?token={WAQI_TOKEN}"
        res = requests.get(url).json()
        return res["data"]["aqi"] if res["status"] == "ok" else None
    except:
        return None

# ------------------ MAIN PREDICTION ENDPOINT ------------------
@app.get("/predict")
def predict():
    """
    Endpoint: /predict
    Does:
    - Fetch data from all 3 APIs
    - Combines and reorders the features correctly (including current AQI)
    - Uses the trained model to predict next-day AQI
    - Returns result as JSON
    """
    try:
        # Step 1: Fetch data from APIs
        pol_data = get_pollutants()
        weather_data = get_weather()
        current_aqi = get_current_aqi()

        if current_aqi is None:
            raise ValueError("Could not fetch current AQI.")

        # Step 2: Combine data into one dict, add current AQI
        full_data = {**pol_data, **weather_data, "AQI": current_aqi}

        # Step 3: Create input DataFrame for prediction
        df = pd.DataFrame([[full_data[feat] for feat in FEATURES]], columns=FEATURES)

        # Step 4: Predict next-day AQI
        pred = model.predict(df)[0]

        return {
            "predicted_next_day_aqi": float(round(pred, 2)),  # convert np.float32 to float
            "current_aqi": current_aqi,
            "input_features": full_data
        }

    except Exception as e:
        return {"error": str(e)}




# ------------------ HEALTH CHECK ROUTE ------------------
@app.get("/")
def home():
    """
    Simple health check endpoint.
    """
    return {"message": "AQI Prediction FastAPI app running."}
