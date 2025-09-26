# app.py
import streamlit as st
import pandas as pd
import requests

API_URL = "http://127.0.0.1:8000"

REQUIRED_FEATURES = [
    "op_setting_1", "op_setting_2",
    "sensor_2", "sensor_3", "sensor_4",
    "sensor_6", "sensor_7", "sensor_8", "sensor_9",
    "sensor_11", "sensor_12", "sensor_13", "sensor_14",
    "sensor_15", "sensor_17", "sensor_20", "sensor_21"
]

# ---- Page Config ----
st.set_page_config(page_title="🔧 Predictive Maintenance", layout="wide", initial_sidebar_state="expanded")

# ---- Custom CSS ----
st.markdown(
    """
    <style>
    body {background-color: #1f1f2e; color: #ffffff;}
    .stButton>button {background-color: #ff4b4b; color: white; border-radius: 10px;}
    .stNumberInput>div>input {background-color: #2b2b3c; color: #ffffff;}
    .stFileUploader>div>input {background-color: #2b2b3c; color: #ffffff;}
    .stDataFrame {background-color: #2b2b3c; color: #ffffff; border-radius: 5px;}
    h1, h2, h3 {color: #ffad33;}
    </style>
    """,
    unsafe_allow_html=True
)

# ---- Sidebar ----
st.sidebar.title("⚙️ Options")
option = st.sidebar.radio("Input Method", ["Upload Log File", "Manual Sensor Input"])

st.title("🚀 Predictive Maintenance Dashboard")
st.markdown("Upload sensor data or enter manually to predict Remaining Useful Life (RUL).")

# ---- Upload Log File ----
if option == "Upload Log File":
    st.info(f"CSV must contain these {len(REQUIRED_FEATURES)} columns:\n\n" + ", ".join(REQUIRED_FEATURES))
    engine_id = st.number_input("Engine ID", min_value=1, step=1)
    uploaded_file = st.file_uploader("Upload Sensor Log (CSV or TXT)", type=["csv", "txt"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())

        if st.button("Predict RUL 🚀"):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
            data = {"engine_id": engine_id}
            response = requests.post(f"{API_URL}/predict/file", files=files, data=data)
            if response.ok:
                result = response.json()
                st.success(f"✅ Predicted RUL: {result['predicted_RUL']:.2f} cycles")
            else:
                st.error(f"❌ API Error: {response.json()['detail']}")

# ---- Manual Input ----
else:
    st.info("Enter all feature values manually.")
    engine_id = st.number_input("Engine ID", min_value=1, step=1)
    
    values = {}
    cols = st.columns(3)
    for idx, feature in enumerate(REQUIRED_FEATURES):
        with cols[idx % 3]:
            values[feature] = st.number_input(feature, value=0.0, format="%.3f")

    if st.button("Predict RUL 🚀"):
        df = pd.DataFrame([values])
        payload = {"engine_id": engine_id, "readings": df.to_dict(orient="records")}
        response = requests.post(f"{API_URL}/predict/sensors", json=payload)
        if response.ok:
            result = response.json()
            st.success(f"✅ Predicted RUL: {result['predicted_RUL']:.2f} cycles")
        else:
            st.error(f"❌ API Error: {response.json()['detail']}")
