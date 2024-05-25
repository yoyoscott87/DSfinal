import requests

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def get_weather_by_coordinates(api_key, lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

api_key = "b55132e7d0d008aa945b18e4cd2f5a02"

# 解析資料
data = """東京,35.6895,139.6917
新北,25.03746,121.564558
台中,24.138504,120.678434
大阪,34.6937249,135.5022535
紐約,40.7127753,-74.0059728
北京,39.9042,116.4074
倫敦,51.5074,-0.1278
巴黎,48.8566,2.3522
台北,25.0330,121.5654
台南,22.9997,120.2269
上海,31.2304,121.4737
洛杉磯,34.0522,-118.2437
高雄,22.6206,120.3120
花蓮,23.9769,121.6049
桃園,24.9937,121.2969
南投,23.9098,120.6840"""

# 將資料轉換為列表
locations = [line.split(",") for line in data.split("\n")]

# 對每個城市獲取天氣資訊
for location in locations:
    city, lat, lon = location
    weather_data = get_weather_by_coordinates(api_key, lat, lon)
    
    temperature_celsius = round(kelvin_to_celsius(weather_data["main"]["temp"]), 1)
    
    print(f"City: {city}")
    print(f"Weather: {weather_data['weather'][0]['description']}")
    print(f"Temperature: {temperature_celsius} °C")
    print(f"Humidity: {weather_data['main']['humidity']} %")
    print()
