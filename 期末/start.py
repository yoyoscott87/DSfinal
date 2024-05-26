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
                response_text_on = turn_12_on()  # 开启第 12 盏灯
                control_air_conditioner_status = "On"
                print(response_text_on)
                print(weather_data["name"],"溫度 :", round(temperature,2), "°C")
                print("溫度超過20度，開啟冷氣")
            else:
                response_text_off = turn_12_off()  # 关闭第 12 盏灯
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


def control_hum_conditioner(humidity):
    try:
        if humidity is not None:
            weather_data = get_weather_by_coordinates(api_key, latitude, longitude)
            if humidity > 60:
                response_text_on = turn_16_on()  # 开启第 16 盏灯
                control_dehumidifier_status = "On"
                print(response_text_on)
                print(weather_data["name"],"濕度 :", round(humidity,2), "%")
                print("濕度高於60%，開啟除濕機")
            elif humidity < 40:
                response_text_off = turn_16_off()  # 关闭第 16 盏灯
                control_dehumidifier_status = "Off"
                print(response_text_off)
                print(weather_data["name"],"濕度 :", round(humidity,2), "%")
                print("濕度低於40%，關閉除濕機")
        else:
            control_dehumidifier_status = "Unknown"
        return control_dehumidifier_status
    except Exception as e:
        print("控制除濕機出錯：", e)
        control_dehumidifier_status = "Error"
        return control_dehumidifier_status
    

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

def turn_14_on():
    url = 'http://211.21.113.190:8155/api/webhook/-lkvcCfPU2wOmNLvhDjrEKpkb'
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI4YWM0MDEzODIwNDU0MDE0ODdjNzIwZTc2ZDBmYzdjYSIsImlhdCI6MTY5ODgwNzExNSwiZXhwIjoyMDE0MTY3MTE1fQ.7KaCwPUcjAr_zne04qili2fwQO1QoWTPzsmV1v_LLIc'
    }

    response = requests.post(url, headers=headers)
    return response.text

# 14 off
def turn_14_off():
    url = 'http://211.21.113.190:8155/api/webhook/-jfyKgpRXg6fgI9IXNIy0GNSn'
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI4YWM0MDEzODIwNDU0MDE0ODdjNzIwZTc2ZDBmYzdjYSIsImlhdCI6MTY5ODgwNzExNSwiZXhwIjoyMDE0MTY3MTE1fQ.7KaCwPUcjAr_zne04qili2fwQO1QoWTPzsmV1v_LLIc'
    }

    response = requests.post(url, headers=headers)
    return response.text


def turn_16_on():
    url = 'http://211.21.113.190:8155/api/webhook/-d2Qi-uvQnpb_KcVcp_Jm9iJK'
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI4YWM0MDEzODIwNDU0MDE0ODdjNzIwZTc2ZDBmYzdjYSIsImlhdCI6MTY5ODgwNzExNSwiZXhwIjoyMDE0MTY3MTE1fQ.7KaCwPUcjAr_zne04qili2fwQO1QoWTPzsmV1v_LLIc'
    }

    response = requests.post(url, headers=headers)
    return response.text

def turn_16_off():
    url = 'http://211.21.113.190:8155/api/webhook/-pAW1x-AJO9s-b9JXDm89Dp_P'
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI4YWM0MDEzODIwNDU0MDE0ODdjNzIwZTc2ZDBmYzdjYSIsImlhdCI6MTY5ODgwNzExNSwiZXhwIjoyMDE0MTY3MTE1fQ.7KaCwPUcjAr_zne04qili2fwQO1QoWTPzsmV1v_LLIc'
    }

    response = requests.post(url, headers=headers)
    return response.text

def get_air_by_coordinates(api_key, lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

def get_air_quality_index(component, value):
    if component == 'so2':
        if value <= 20:
            return 0
        elif value <= 80:
            return 1
        elif value <= 250:
            return 2
        elif value <= 350:
            return 3
        else:
            return 4
    elif component == 'no2':
        if value <= 40:
            return 0
        elif value <= 70:
            return 1
        elif value <= 150:
            return 2
        elif value <= 200:
            return 3
        else:
            return 4
    elif component == 'pm10':
        if value <= 20:
            return 0
        elif value <= 50:
            return 1
        elif value <= 100:
            return 2
        elif value <= 200:
            return 3
        else:
            return 4
    elif component == 'pm2_5':
        if value <= 10:
            return 0
        elif value <= 25:
            return 1
        elif value <= 50:
            return 2
        elif value <= 75:
            return 3
        else:
            return 4
    elif component == 'o3':
        if value <= 60:
            return 0
        elif value <= 100:
            return 1
        elif value <= 140:
            return 2
        elif value <= 180:
            return 3
        else:
            return 4
    elif component == 'co':
        if value <= 4400:
            return 0
        elif value <= 9400:
            return 1
        elif value <= 12400:
            return 2
        elif value <= 15400:
            return 3
        else:
            return 4
    
    else:
        return 'Unknown'

def map_score_to_level(score):
    if score <= 1:
        return "優秀"
    elif score <= 2:
        return "良好"
    elif score <= 3:
        return "一般"
    else:
        return "差"
    
def air_control(air_quality_level):
    if air_quality_level == "優秀"or air_quality_level == "良好":
        response_text_on = turn_14_on()  # 開啟空氣清新機
        print("空氣品質良好，" + response_text_on)
    

    elif air_quality_level == "一般" or air_quality_level == "差":
        response_text_off = turn_14_off()  # 關閉空氣清新機
        print("空氣品質一般，" + response_text_off)
    else:
        print("未知空氣品質等級")
                
    
def server():
    while True:
        try:
            weather_data = get_weather_by_coordinates(api_key, latitude, longitude)
            if weather_data is not None:
                temperature_celsius = kelvin_to_celsius(weather_data["main"]["temp"])
                hum_celsius = weather_data["main"]["humidity"]
                air_conditioner_status = control_air_conditioner(temperature_celsius)
                control_dehumidifier_status = control_hum_conditioner(hum_celsius)

                #空氣品質
                air_data = get_air_by_coordinates(api_key, latitude, longitude)
                components = air_data['list'][0]['components']

                total_score = 0
                for component, value in components.items():
                    if component in weights:
                        aqi_score = get_air_quality_index(component, value)
                        total_score += aqi_score * weights[component]
                
                # 將評分映射到等級
                air_quality_level = map_score_to_level(total_score)
                print("空氣品質等級:", air_quality_level)


                # 将数据写入 Google Sheets
                sheet.append_row([weather_data["name"], f"{round(temperature_celsius,2)}\u2103",f"{round(hum_celsius,2)}%" ,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),air_conditioner_status,control_dehumidifier_status, air_quality_level])
        except Exception as e:
            print("Error:", e)
        time.sleep(300)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
client = gspread.authorize(credentials)
sheet = client.open("DSfinal").sheet1
file_path = '經緯度參考.txt'
locations = read_coordinates_from_file(file_path)
location_name = "東京"
latitude, longitude = get_coordinates_by_location(location_name)
weights = {'so2': 0.1, 'no2': 0.15, 'pm10': 0.2, 'pm2_5': 0.25, 'o3': 0.15, 'co': 0.15}

#latitude = 51.5074
#longitude = -0.1278
server()