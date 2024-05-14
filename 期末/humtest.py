import requests
import json

def get_weather_data(api_key, latitude, longitude):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code)
        return None

api_key = "b55132e7d0d008aa945b18e4cd2f5a02"
latitude = 35.689381
longitude = 139.69181
weather_data = get_weather_data(api_key, latitude, longitude)

if weather_data:
    print(json.dumps(weather_data, indent=4))  # 打印原始的 JSON 数据