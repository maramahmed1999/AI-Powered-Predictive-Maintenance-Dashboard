# AI Powered Predictive Maintenance Dashboard
Machine learning project designed to predict the health status and remaining useful life (RUL) of industrial equipment using time-series sensor data. 
The system is built on the NASA CMAPSS Turbofan Jet Engine dataset, which contains multiple operating conditions and fault modes.

---
  
##Our pipeline includes:

###🔧 Data Preparation & Cleaning: 
- Handling missing values, aligning time-series, and preparing run-to-failure windows.

###📊 Exploratory Data Analysis (EDA): 
- Identifying sensor trends, degradation patterns, and operating condition effects.

###🤖 Model Training: 
- Implementing both traditional ML models (e.g., Gradient Boosting, Random Forests) and deep learning approaches (e.g., LSTM networks) to predict either:

    - Remaining Useful Life (RUL) → regression framing

    - Failure risk (healthy/faulty) → classification framing

###✅ Model Validation: 
- performance evaluation using time-series metrics such as RMSE, MAE, and accuracy.

###🌐 Deployment: 
- A lightweight Streamlit dashboard where users can upload sensor logs in CSV format and receive real-time health forecasts or maintenance risk alerts.

---

This project demonstrates how predictive maintenance can reduce unplanned downtime, optimize maintenance schedules, and save costs in real-world industrial settings.
