function kelvinToCelsius(kelvin) {
    return kelvin - 273.15;
}

function getWeatherByCoordinates(apiKey, lat, lon) {
    const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${apiKey}`;
    return fetch(url)
        .then(response => response.json())
        .then(data => data);
}

document.getElementById('search-button').addEventListener('click', function() {
    const apiKey = 'b55132e7d0d008aa945b18e4cd2f5a02';
    const city = document.getElementById('city-input').value.trim();
    const locations = {
        "東京": [35.6895, 139.6917],
        "新北": [25.03746, 121.564558],
        "台中": [24.138504, 120.678434],
        "大阪": [34.6937249, 135.5022535],
        "紐約": [40.7127753, -74.0059728],
        "北京": [39.9042, 116.4074],
        "倫敦": [51.5074, -0.1278],
        "巴黎": [48.8566, 2.3522],
        "台北": [25.0330, 121.5654],
        "台南": [22.9997, 120.2269],
        "上海": [31.2304, 121.4737],
        "洛杉磯": [34.0522, -118.2437],
        "高雄": [22.6206, 120.3120],
        "花蓮": [23.9769, 121.6049],
        "桃園": [24.9937, 121.2969],
        "南投": [23.9098, 120.6840]
    };

    if (locations[city]) {
        const [lat, lon] = locations[city];
        getWeatherByCoordinates(apiKey, lat, lon).then(weatherData => {
            const temperatureCelsius = Math.round(kelvinToCelsius(weatherData["main"]["temp"]) * 10) / 10;
            document.getElementById('city-name').textContent = city;
            document.getElementById('temperature').textContent = temperatureCelsius;
            document.getElementById('humidity').textContent = weatherData["main"]["humidity"];
            document.getElementById('air-quality').textContent = 'N/A'; // 空氣品質資料需要另外的 API
            document.getElementById('weather-forecast').src = ''; // 這裡可以添加天氣預測圖的 URL
            document.getElementById('pressure-chart').src = ''; // 這裡可以添加氣壓圖的 URL
        }).catch(error => {
            console.error('Error fetching weather data:', error);
        });
    } else {
        alert('未找到該城市的天氣數據');
    }
});

document.getElementById('ac-button').addEventListener('click', function() {
    alert('冷氣已開啟/關閉');
});

document.getElementById('dehumidifier-button').addEventListener('click', function() {
    alert('除濕機已開啟/關閉');
});
