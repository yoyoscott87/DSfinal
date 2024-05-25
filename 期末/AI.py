from flask import Flask, render_template, request, jsonify
import requests
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# 设置 Google Sheets API 认证信息
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('sincere-venture-419101-185a586d9858.json', scope)
client = gspread.authorize(creds)

# 打开 Google 表格并选择工作表
sheet = client.open('DSfinal').sheet1
data = sheet.get_all_records()

# 根据数据构建模型的输入
prompt = ""
for row in data:
    prompt += f"在{row['地點']}的{row['時間']}，溫度是{row['溫度(°C)']}，濕度是{row['濕度']}，空氣品質是{row['空氣品質']}，冷氣狀況是{row['冷氣狀況(12燈)']}，除濕機狀況是{row['除濕機狀況(16燈)']}；"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    # 获取用户提出的问题
    question = request.form['question']
    
    # 根据问题构建模型的输入
    prompt_with_question = f"{prompt} 用户问：{question}"
    
    # 调用模型生成答案
    url = "http://localhost:5000/v1/completions"
    headers = {"Content-Type": "application/json"}
    model_data = {
        "model": "v2_1.gguf",
        "prompt": prompt_with_question,
        "max_tokens": 100,
        "stop": ["。", "？", "!"]  # 添加停止标记
    }
    response = requests.post(url, headers=headers, data=json.dumps(model_data))
    answer = response.json()['choices'][0]['text'].strip()
    
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
