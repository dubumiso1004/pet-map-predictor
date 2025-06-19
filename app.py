import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
import cloudpickle

# ------------------ 1. 모델 로딩 ------------------
@st.cache_resource
def load_model():
    with open("pet_rf_model_full.pkl", "rb") as f:
        return cloudpickle.load(f)
model = load_model()

# ------------------ 2. 측정 데이터 로딩 ------------------
def dms_to_decimal(dms_str):
    parts = list(map(float, str(dms_str).split(";")))
    return parts[0] + parts[1]/60 + parts[2]/3600

df = pd.read_excel("total_svf_gvi_bvi_250613.xlsx", sheet_name="gps 포함")
df["Lat_decimal"] = df["Lat"].apply(dms_to_decimal)
df["Lon_decimal"] = df["Lon"].apply(dms_to_decimal)

# ------------------ 3. 최근접 지점 SVF/GVI/BVI 추정 함수 ------------------
def get_nearest_svf_gvi_bvi(lat, lon):
    df["distance"] = ((df["Lat_decimal"] - lat)**2 + (df["Lon_decimal"] - lon)**2)**0.5
    nearest = df.loc[df["distance"].idxmin()]
    return nearest["SVF"], nearest["GVI"], nearest["BVI"]

# ------------------ 4. Streamlit UI ------------------
st.set_page_config(layout="wide")
st.title("🗺️ 부산대학교 지도 기반 PET 예측")

# 지도 표시 (부산대학교 건설관 기준)
m = folium.Map(location=[35.2323, 129.0797], zoom_start=17)
m.add_child(folium.LatLngPopup())
st_data = st_folium(m, width=700, height=500)

# ------------------ 5. 사용자 클릭 처리 ------------------
if st_data["last_clicked"]:
    lat = st_data["last_clicked"]["lat"]
    lon = st_data["last_clicked"]["lng"]

    svf, gvi, bvi = get_nearest_svf_gvi_bvi(lat, lon)

    st.info(f"📍 클릭 위치: 위도 {lat:.6f}, 경도 {lon:.6f}")
    st.write(f"☀️ 추정 SVF: {svf:.3f}, 🌿 GVI: {gvi:.3f}, 🏢 BVI: {bvi:.3f}")

    # 고정 기상 입력값
    air_temp = 25.0
    humidity = 50.0
    wind_speed = 1.0

    # 예측 실행
    input_df = pd.DataFrame([{
        "SVF": svf, "GVI": gvi, "BVI": bvi,
        "AirTemperature": air_temp,
        "Humidity": humidity,
        "WindSpeed": wind_speed
    }])
    pet = model.predict(input_df)[0]
    st.success(f"🔥 예측 PET: {pet:.2f} °C")
