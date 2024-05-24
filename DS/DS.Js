function parseWeatherData(data) {
    const lines = data.split('\n');
    const weatherData = {};

    lines.forEach(line => {
        if (line.trim() !== '') {
            const [cityPart, ...weatherParts] = line.split('，');
            const city = cityPart.replace('在', '').trim();
            const weatherPart = weatherParts.join('，');
            const temperatureMatch = weatherPart.match(/温度是([\d.-]+)℃/);
            const humidityMatch = weatherPart.match(/濕度是([\d%]+)%/);
            const timeMatch = weatherPart.match(/時間是([\d-: ]+)/);
            const acStatusMatch = weatherPart.match(/冷氣狀況是(\w+)/);
            const dehumidifierStatusMatch = weatherPart.match(/除濕機狀況是(\w+)/);
            const airQualityMatch = weatherPart.match(/空氣品質是([\w]+)/);

            weatherData[city] = {
                temperature: temperatureMatch ? temperatureMatch[1] : 'N/A',
                humidity: humidityMatch ? humidityMatch[1] : 'N/A',
                time: timeMatch ? timeMatch[1] : 'N/A',
                acStatus: acStatusMatch ? acStatusMatch[1] : 'N/A',
                dehumidifierStatus: dehumidifierStatusMatch ? dehumidifierStatusMatch[1] : 'N/A',
                airQuality: airQualityMatch ? airQualityMatch[1] : 'N/A'
            };
        }
    });

    return weatherData;
}

document.getElementById('search-button').addEventListener('click', function() {
    fetch('train.txt')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(data => {
            const weatherData = parseWeatherData(data);
            const city = document.getElementById('city-input').value.trim();

            if (weatherData[city]) {
                const weather = weatherData[city];
                document.getElementById('city-name').textContent = city;
                document.getElementById('temperature').textContent = weather.temperature;
                document.getElementById('humidity').textContent = weather.humidity;
                document.getElementById('air-quality').textContent = weather.airQuality;
                // 這裡沒有天氣圖標和氣壓圖表URL的數據，暫時保留空白
                document.getElementById('weather-forecast').src = '';
                document.getElementById('pressure-chart').src = '';
            } else {
                alert('未找到該城市的天氣數據');
            }
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
        });
});

document.getElementById('ac-button').addEventListener('click', function() {
    alert('冷氣已開啟/關閉');
});

document.getElementById('dehumidifier-button').addEventListener('click', function() {
    alert('除濕機已開啟/關閉');
});
