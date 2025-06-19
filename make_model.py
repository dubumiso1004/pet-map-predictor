import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import cloudpickle

# 1. 데이터 불러오기
df = pd.read_excel("total_svf_gvi_bvi_250613.xlsx", sheet_name="gps 포함")

# 2. 입력 변수(X)와 타겟 변수(y) 나누기
X = df[["SVF", "GVI", "BVI", "AirTemperature", "Humidity", "WindSpeed"]]
y = df["PET"]

# 3. 모델 생성 및 학습
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# 4. 모델 저장
with open("pet_rf_model_full.pkl", "wb") as f:
    cloudpickle.dump(model, f)

print("✅ 모델 저장 완료: pet_rf_model_full.pkl")
