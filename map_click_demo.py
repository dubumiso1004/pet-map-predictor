import streamlit as st
from streamlit_folium import st_folium
import folium

st.set_page_config(layout="wide")
st.title("🗺️ 지도 클릭으로 위치 선택")

# 지도 생성
m = folium.Map(location=[35.13, 129.05], zoom_start=16)

# 클릭 이벤트 추가
m.add_child(folium.LatLngPopup())  # 클릭한 위치 위경도 팝업으로 보여줌

# Streamlit 앱에 지도 표시
st_data = st_folium(m, width=700, height=500)

# 클릭된 위치의 위경도 표시
if st_data["last_clicked"]:
    lat = st_data["last_clicked"]["lat"]
    lon = st_data["last_clicked"]["lng"]
    st.success(f"📍 클릭한 위치: 위도 {lat:.6f}, 경도 {lon:.6f}")
