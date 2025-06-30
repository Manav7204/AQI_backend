# 🌫️ AQI Prediction Web App

A simple, responsive web application that predicts the next day's **Air Quality Index (AQI)** for **Mumbai** using a **Polynomial Regression model**, with real-time weather and pollutant data.

---

## 🚀 Features

- ✅ Real-time pollutant & weather data from OpenWeatherMap & WAQI APIs
- ✅ Next-day AQI prediction using a trained ML model
- ✅ Clean, responsive frontend with scrollable UI
- ✅ Informative AQI category table and visuals
- ✅ FastAPI backend + Vercel frontend + Render backend hosting

---

## 🧠 Machine Learning Model

- **Type**: Polynomial Regression  
- **Library**: Scikit-learn  
- **Trained On**: Preprocessed dataset of AQI + weather + pollutant features  
- **Model File**: `aqi_model.joblib`

---

## 📦 Tech Stack

| Layer      | Technology                              |
|------------|-----------------------------------------| 
| Frontend   | HTML, CSS, JavaScript                   |
| Backend    | FastAPI (Python)                        |
| ML Model   | Polynomial Regression                   |
| Hosting    | Vercel (frontend), Render (backend API) |
| APIs Used  | OpenWeatherMap, WAQI                    |

---

## 📁 Project Structure
AQI_Prediction/
├── main.py # FastAPI backend
├── requirements.txt # Backend dependencies
├── models/
│ └── aqi_model.joblib # Trained regression model
├── Frontend/
│ ├── index.html
│ ├── style.css
│ └── script.js

---

## ⚙️ How It Works

1. User selects **Mumbai** and clicks “Predict”
2. Frontend calls FastAPI `/predict` endpoint (hosted on Render)
3. FastAPI fetches current pollutant/weather data from APIs
4. Model predicts next-day AQI
5. Frontend displays prediction, current AQI, inputs used, and more

---

## 🔗 Live Demo

Frontend: [aqi-ui-manav.vercel.app](https://your-vercel-link.vercel.app)  
Backend API: [aqi-api-manav.onrender.com](https://your-render-link.onrender.com/predict)

---

## 🙌 Author

👤 **Manav Patil**  
📧 [Email]: patilmanav1282@gmail.com
💼 [LinkedIn](www.linkedin.com/in/manav-patil-51a604226)
🎓 Computer Engineering | Bharati Vidyapeeth College of Engineering  

