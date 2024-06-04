# DS final
2024/05/07




- [test.py](期末/test.py)是 text-to-sound(文字轉聲音)測試，測試檔是[speech.wav](期末/speech.wav)


- [weather.ipynb](期末/weather.ipynb)是在測試用API獲取某地資料

2024/05/10


-  主程式放在[start.py](期末/start.py)，run下去能做判斷開關燈，拿天氣資訊
-  天氣測試程式放在[weather.ipynb](期末/weather.ipynb)
-  高溫警報  設計網頁
-  [生成天氣預報圖](https://openweathermap.org/widgets-constructor)
-  [氣壓圖](https://openweathermap.org/api/weathermaps)
-  網頁 : 輸入格(想查詢之城市) 天氣預測圖，氣壓圖，開關燈按鈕，當時氣溫濕度

2024/05/11

-  加入濕度判斷
-  要run程式ㄉ話，跟我要.env檔，不然你們在自己ㄉ電腦上不能跑

2024/05/14

-  擴增功能，多利用api給ㄉ資訊
-  [api給的資訊](https://openweathermap.org/current)
-  加濕器

2024/06/04
-  天氣資訊網期末demo
-  [網頁](flask/templates/index.html)  [JS](static/scripts.js)和[CSS](static/styles.css)
-  [主程式](flask/AI.py)
-  利用curl方式或的辦公室氣溫濕度，判斷之後使用curl控制燈泡代表家電
   
      用openweather api獲取天氣資訊，提供使用者相關氣象，出門前使用

      天氣管家，利用LM stdio串接hugging face語言模型，實現問答對話

      google sheet記錄使用者使用紀錄，當作後端資料庫

