from flask import Flask, render_template, request, jsonify
import requests
import json
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

# 設置Google Sheets API認證
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('flask\sincere-venture-419101-185a586d9858.json', scope)
client = gspread.authorize(credentials)
sheet = client.open('test').sheet1
weights = {'so2': 0.1, 'no2': 0.15, 'pm10': 0.2, 'pm2_5': 0.25, 'o3': 0.15, 'co': 0.15}
# 獲取OpenWeather API密鑰
api_key = os.getenv("API_KEY")

# 讀取經緯度數據
file_path = 'flask\經緯度參考.txt'
#辦公室
authorization_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI4YWM0MDEzODIwNDU0MDE0ODdjNzIwZTc2ZDBmYzdjYSIsImlhdCI6MTY5ODgwNzExNSwiZXhwIjoyMDE0MTY3MTE1fQ.7KaCwPUcjAr_zne04qili2fwQO1QoWTPzsmV1v_LLIc"
api_endpoint_tem = "http://211.21.113.190:8155/api/states/sensor.ban_gong_shi_wen_shi_du_temperature"
api_endpoint_hum = "http://211.21.113.190:8155/api/states/sensor.ban_gong_shi_wen_shi_du_humidity"
headers = {"Authorization": "Bearer " + authorization_token}



@app.route('/')
def index():
    return render_template('index.html')


def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def get_weather_data(api_key, lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def read_coordinates_from_file(file_path):
    coordinates = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(',')
            place_name = parts[0]
            latitude, longitude = map(float, parts[1:])
            coordinates[place_name] = (latitude, longitude)
    return coordinates

def get_air_by_coordinates(api_key, lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

def turn_14_on():
    url = 'http://211.21.113.190:8155/api/webhook/-lkvcCfPU2wOmNLvhDjrEKpkb'
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI4YWM0MDEzODIwNDU0MDE0ODdjNzIwZTc2ZDBmYzdjYSIsImlhdCI6MTY5ODgwNzExNSwiZXhwIjoyMDE0MTY3MTE1fQ.7KaCwPUcjAr_zne04qili2fwQO1QoWTPzsmV1v_LLIc'
    }

    response = requests.post(url, headers=headers)
    return response.text

def turn_14_off():
    url = 'http://211.21.113.190:8155/api/webhook/-jfyKgpRXg6fgI9IXNIy0GNSn'
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI4YWM0MDEzODIwNDU0MDE0ODdjNzIwZTc2ZDBmYzdjYSIsImlhdCI6MTY5ODgwNzExNSwiZXhwIjoyMDE0MTY3MTE1fQ.7KaCwPUcjAr_zne04qili2fwQO1QoWTPzsmV1v_LLIc'
    }

    response = requests.post(url, headers=headers)
    return response.text

response_text_off = turn_14_off()  # 關閉第 14 盞燈
print(response_text_off)

response_text_on = turn_14_on()  # 開啟第 14 盞燈
print(response_text_on)


def log_to_google_sheet(data):
    try:
        # 追加一行到 Google Sheets
        sheet.append_row(data)
        print("成功記錄到 Google Sheets")
    except Exception as e:
        print(f"記錄到 Google Sheets 時出錯: {e}")


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

def get_weather(api_key, latitude, longitude):
    try:
        weather_data = get_weather_data(api_key, latitude, longitude)  # 假設這個函數是存在的，並且根據 API 提供天氣資料
        temperature = kelvin_to_celsius(weather_data["main"]["temp"])
        humidity = weather_data["main"]["humidity"]
        weather_description = weather_data["weather"][0]["description"]
        air_data = get_air_by_coordinates(api_key, latitude, longitude)
        components = air_data['list'][0]['components']
        total_score = 0
        for component, value in components.items():
            if component in weights:
                aqi_score = get_air_quality_index(component, value)
                total_score += aqi_score * weights[component]
                    
                # 將評分映射到等級
        air_quality_level = map_score_to_level(total_score)

        print(f"地點: {weather_data['name']}")
        print(f"溫度: {round(temperature, 2)} °C")
        print(f"濕度: {humidity} %")
        print(f"天氣: {weather_description}")
        print(f"空氣品質:{air_quality_level}")

        log_data = [
            time.strftime("%Y-%m-%d %H:%M:%S"),  # 当前时间
            weather_data['name'],  # 地點
            round(temperature, 2),  # 溫度
            humidity,  # 濕度
            air_quality_level  # 空氣品質
        ]
        log_to_google_sheet(log_data)

        return {
            "temperature": round(temperature, 2),
            "humidity": humidity,
            "weather_description": weather_description,
            "air": air_quality_level
        }
    except requests.exceptions.RequestException as e:
        print("API請求出錯：", e)
        return None
    except KeyError as e:
        print("JSON解析出錯：", e)
        return None
    except Exception as e:
        print("未知錯誤：", e)
        return None

@app.route('/weather', methods=['POST'])
def weather():
    locations = read_coordinates_from_file(file_path)
    data = request.json
    location_name = data.get('city')  
    if location_name in locations:
        latitude, longitude = locations[location_name]
        weather_data = get_weather(api_key, latitude, longitude)  # 調用修改後的函數來獲取天氣資料
        if weather_data:
            locweather_data = {
                'city': location_name,
                'weather_description': weather_data["weather_description"],
                'temperature': weather_data["temperature"],
                'humidity': weather_data["humidity"],
                'air': weather_data["air"]
            }
            return jsonify(locweather_data)
        else:
            return jsonify({'error': 'Failed to get weather data'})
    else:
        print("地點名稱無效")
        return jsonify({'error': 'Invalid location name'})

# 構建模型的輸入
data = sheet.get_all_records()
prompt = ""
prompt += f"在Osaka的空氣品質，時間2024-05-25 12:54，是什麼水準？"
prompt += f"Osaka在資料中被記錄了幾次?2次"
prompt += f"Toyko的最高溫出現在甚麼時候?23.68(°C)在時間2024-05-19 10:54:12"

for row in data:
        prompt += f"在{row['時間']}的{row['地點']}溫度是{row['溫度(°C)']}，濕度是{row['濕度']}，空氣品質是{row['空氣品質']}，冷氣的狀態是{row['冷氣狀況(12燈)']}，除濕機的狀態是{row['除濕機狀況(16燈)']}"




def get_tem():
    try:
        response = requests.get(api_endpoint_tem, headers=headers)
        response.raise_for_status()  # 檢查HTTP請求是否成功
        data = response.json()
        temperature = float(data["state"])
        print("溫度：", temperature)
        return temperature
    except requests.exceptions.RequestException as e:
        print("請求出錯：", e)
        return None

def get_hum():
    try:
        response = requests.get(api_endpoint_hum, headers=headers)
        response.raise_for_status()  # 檢查HTTP請求是否成功
        data = response.json()
        humidity = float(data["state"])
        print("濕度：", humidity)
        return humidity
    except requests.exceptions.RequestException as e:
        print("請求出錯：", e)
        return None

def control_air(temperature):
    try:
        if temperature is not None:
            if temperature > 23:
                response_text_on = control_device("on", "12")
                print(response_text_on)
                print("溫度超過 23 度，開啟冷氣")
                return "開啟"
            else:
                response_text_off = control_device("off", "12")
                print(response_text_off)
                print("溫度低於等於 23 度，關閉冷氣")
                return "關閉"
    except Exception as e:
        print("控制冷氣出錯：", e)

def control_hum(humidity):
    try:
        if humidity is not None:
            if humidity > 60:
                response_text_on = control_device("on", "16")
                print(response_text_on)
                print("濕度大於 60%，開啟除濕機")
                return "開啟"
            elif humidity < 40:
                response_text_off = control_device("off", "16")
                print(response_text_off)
                print("濕度低於 40%，關閉除濕機")
                return "關閉"
    except Exception as e:
        print("控制除濕機出錯：", e)

def control_device(action, device_id):
    base_url = 'http://211.21.113.190:8155/api/webhook/'
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI4YWM0MDEzODIwNDU0MDE0ODdjNzIwZTc2ZDBmYzdjYSIsImlhdCI6MTY5ODgwNzExNSwiZXhwIjoyMDE0MTY3MTE1fQ.7KaCwPUcjAr_zne04qili2fwQO1QoWTPzsmV1v_LLIc"

    url = f'{base_url}{get_device_url(action, device_id)}'
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.post(url, headers=headers)
    return response.text

def get_device_url(action, device_id):
    urls = {
        '12': {
            'on': '-TJO7MQn5u--KlqSH4Mw2JHA7',
            'off': '-jAxX99jM2ghu4SVD29Ht8Flx'
        },
        '16': {
            'on': '-d2Qi-uvQnpb_KcVcp_Jm9iJK',
            'off': '-pAW1x-AJO9s-b9JXDm89Dp_P'
        }
    }
    return urls[device_id][action]

@app.route('/auto', methods=['GET'])
def auto_control():
    temperature = get_tem()
    humidity = get_hum()

    if temperature is not None:
        air_conditioner_status = control_air(temperature)
    if humidity is not None:
        dehumidifier_status = control_hum(humidity)
    
    log_data = [
        time.strftime("%Y-%m-%d %H:%M:%S"),  # 当前时间
        "辦公室",  
        temperature,  # 温度
        humidity,  # 湿度
        air_conditioner_status,  # 冷气状态
        dehumidifier_status  # 除湿机状态
    ]
    log_to_google_sheet(log_data)


    return jsonify({
        'status': 'success',
        'temperature': temperature,
        'humidity': humidity,
        'air_conditioner': air_conditioner_status,
        'dehumidifier': dehumidifier_status
    })

@app.route('/toggle_air_conditioner', methods=['POST'])
def toggle_air_conditioner():
    try:
        current_status = request.json.get('current_status')
        device_id = "12"  

        # 反转冷气状态
        if current_status == "開啟":
            response_text = control_device("off", device_id)
            new_status = "關閉"
        else:
            response_text = control_device("on", device_id)
            new_status = "開啟"

        return jsonify({
            'status': 'success',
            'new_status': new_status
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/toggle_hum', methods=['POST'])
def toggle_hum():
    try:
        current_status = request.json.get('current_status')
        device_id = "16"  

        print(f"Received current_status: {current_status}") 

        if current_status == "開啟":
            response_text = control_device("off", device_id)
            new_status = "關閉"
        else:
            response_text = control_device("on", device_id)
            new_status = "開啟"

        print(f"Toggled dehumidifier to: {new_status}")  

        return jsonify({
            'status': 'success',
            'new_status': new_status
        })
    except Exception as e:
        print(f"Error in toggle_hum: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question']
    prompt_with_question = f"{prompt}{question}"
    
    url = "http://localhost:1234/v1/completions"
    headers = {"Content-Type": "application/json"}
    model_data = {
        "model": "audreyt/Breeze-7B-Instruct-64k-v0.1-GGUF",
        "prompt": prompt_with_question,
        "max_tokens": 400,
        "stop": ["。", "？", "!"]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(model_data))

        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            return jsonify({'error': 'Failed to get response from the model API'}), 500

        response_data = response.json()

        if 'choices' not in response_data or not response_data['choices']:
            return jsonify({'error': 'No choices found in response'}), 500

        answer = response_data['choices'][0]['text'].strip()
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
    
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
    