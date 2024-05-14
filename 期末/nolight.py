import requests
def turn_16_off():
    url = 'http://211.21.113.190:8155/api/webhook/-pAW1x-AJO9s-b9JXDm89Dp_P'
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI4YWM0MDEzODIwNDU0MDE0ODdjNzIwZTc2ZDBmYzdjYSIsImlhdCI6MTY5ODgwNzExNSwiZXhwIjoyMDE0MTY3MTE1fQ.7KaCwPUcjAr_zne04qili2fwQO1QoWTPzsmV1v_LLIc'
    }

    response = requests.post(url, headers=headers)
    return response.text

response_text_off = turn_16_off()  # 關閉第 16 盞燈
print(response_text_off)

def turn_12_off():
    url = 'http://211.21.113.190:8155/api/webhook/-jAxX99jM2ghu4SVD29Ht8Flx'
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI4YWM0MDEzODIwNDU0MDE0ODdjNzIwZTc2ZDBmYzdjYSIsImlhdCI6MTY5ODgwNzExNSwiZXhwIjoyMDE0MTY3MTE1fQ.7KaCwPUcjAr_zne04qili2fwQO1QoWTPzsmV1v_LLIc'
    }

    response = requests.post(url, headers=headers)
    return response.text

response_text_off = turn_12_off()  # 關閉第 12 盞燈
print(response_text_off)



while True:
    # 呼叫 turn_l2_off() 函數
    turn_12_off()
    
    # 呼叫 turn_16_off() 函數
    turn_16_off()