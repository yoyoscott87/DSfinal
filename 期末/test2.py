#獲得某地天氣資料後做判斷開關燈，先做著可以想想要不要用
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import time
import os
from dotenv import load_dotenv
load_dotenv()

credentials_file = os.getenv("CREDENTIALS_FILE")
api_key = os.getenv("API_KEY")

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

# 从文件中读取地点名称和经纬度信息
def read_coordinates_from_file(file_path):
    coordinates = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(',')
            place_name = parts[0]
            latitude, longitude = map(float, parts[1:])
            coordinates[place_name] = (latitude, longitude)
    return coordinates

def get_coordinates_by_location(location_name):
    if location_name in locations:
        return locations[location_name]
    else:
        print("地點名稱無效")
        return None

def get_weather_by_coordinates(api_key, lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

#判斷開關燈
def control_air_conditioner(temperature):
    try:
        if temperature is not None:
            weather_data = get_weather_by_coordinates(api_key, latitude, longitude)
            if temperature > 20:
                response_text_on = turn_12_on()  # 开启第 16 盏灯
                control_air_conditioner_status = "On"
                print(response_text_on)
                print(weather_data["name"],"溫度 :", round(temperature,2), "°C")
                print("溫度超過20度，開啟冷氣")
            else:
                response_text_off = turn_12_off()  # 关闭第 16 盏灯
                control_air_conditioner_status = "Off"
                print(response_text_off)
                print(weather_data["name"],"溫度 :", round(temperature,2), "°C")
                print("溫度低於20度，關閉冷氣")
        else:
            control_air_conditioner_status = "Unknown"
        return control_air_conditioner_status
    except Exception as e:
        print("控制冷氣出錯：", e)
        control_air_conditioner_status = "Error"
        return control_air_conditioner_status


def turn_12_on():
    url = 'http://211.21.113.190:8155/api/webhook/-TJO7MQn5u--KlqSH4Mw2JHA7'
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI4YWM0MDEzODIwNDU0MDE0ODdjNzIwZTc2ZDBmYzdjYSIsImlhdCI6MTY5ODgwNzExNSwiZXhwIjoyMDE0MTY3MTE1fQ.7KaCwPUcjAr_zne04qili2fwQO1QoWTPzsmV1v_LLIc'
    }

    response = requests.post(url, headers=headers)
    return response.text

def turn_12_off():
    url = 'http://211.21.113.190:8155/api/webhook/-jAxX99jM2ghu4SVD29Ht8Flx'
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI4YWM0MDEzODIwNDU0MDE0ODdjNzIwZTc2ZDBmYzdjYSIsImlhdCI6MTY5ODgwNzExNSwiZXhwIjoyMDE0MTY3MTE1fQ.7KaCwPUcjAr_zne04qili2fwQO1QoWTPzsmV1v_LLIc'
    }

    response = requests.post(url, headers=headers)
    return response.text

def server():
    while True:
        try:
            weather_data = get_weather_by_coordinates(api_key, latitude, longitude)
            if weather_data is not None:
                temperature_celsius = kelvin_to_celsius(weather_data["main"]["temp"])
                air_conditioner_status = control_air_conditioner(temperature_celsius)

                # 将数据写入 Google Sheets
                sheet.append_row([weather_data["name"], f"{round(temperature_celsius,2)}\u2103", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),air_conditioner_status])
        except Exception as e:
            print("Error:", e)
        time.sleep(30) 

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
client = gspread.authorize(credentials)
sheet = client.open("DSfinal").sheet1
file_path = '經緯度參考.txt'
locations = read_coordinates_from_file(file_path)
location_name = "紐約"
latitude, longitude = get_coordinates_by_location(location_name)

# 替换为你希望获取天气数据的地点的经纬度坐标
#latitude = 34.6937249
#longitude = 135.5022535
server()