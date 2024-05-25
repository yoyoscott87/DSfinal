function kelvinToCelsius(kelvin) {
    return kelvin - 273.15;
}

function getCityIdByName(apiKey, cityName) {
    const url = `https://api.openweathermap.org/data/2.5/find?q=${cityName}&appid=${apiKey}`;
    return fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.list && data.list.length > 0) {
                return data.list[0].id; // Return the first city's ID
            } else {
                throw new Error('City not found');
            }
        });
}

function getWeatherByCityId(apiKey, cityId) {
    const url = `https://api.openweathermap.org/data/2.5/weather?id=${cityId}&appid=${apiKey}&units=metric`;
    return fetch(url)
        .then(response => response.json())
        .then(data => data);
}

function updateWeatherWidget(cityId) {
    // Clear previous widget parameters
    window.myWidgetParam = [];
    window.myWidgetParam.push({
        id: 11,
        cityid: cityId,
        appid: 'b55132e7d0d008aa945b18e4cd2f5a02',
        units: 'metric',
        containerid: 'openweathermap-widget-11',
    });

    // Remove old widget container and add a new one
    const widgetContainer = document.getElementById('openweathermap-widget-11');
    const newWidgetContainer = widgetContainer.cloneNode(false);
    widgetContainer.parentNode.replaceChild(newWidgetContainer, widgetContainer);

    // Add new script
    const script = document.createElement('script');
    script.async = true;
    script.charset = "utf-8";
    script.src = "//openweathermap.org/themes/openweathermap/assets/vendor/owm/js/weather-widget-generator.js";
    script.id = 'weather-widget-script';
    const s = document.getElementsByTagName('script')[0];
    s.parentNode.insertBefore(script, s);
}

function updatePressureChart(apiKey) {
    const z = 5; // Example zoom level
    const x = 10; // Example x coordinate
    const y = 10; // Example y coordinate
    const chartImg = document.getElementById('pressure-chart-img');
    const chartUrl = `https://tile.openweathermap.org/map/pressure_new/${z}/${x}/${y}.png?appid=${apiKey}`;
    chartImg.src = chartUrl;
    chartImg.alt = `氣壓圖`;
}

document.getElementById('search-button').addEventListener('click', function() {
    const cityName = document.getElementById('city-input').value.trim();
    const apiKey = 'b55132e7d0d008aa945b18e4cd2f5a02';

    getCityIdByName(apiKey, cityName).then(cityId => {
        return getWeatherByCityId(apiKey, cityId).then(weatherData => {
            document.getElementById('city-name').textContent = weatherData.name;
            document.getElementById('temperature').textContent = weatherData.main.temp;
            document.getElementById('humidity').textContent = weatherData.main.humidity;
            updateWeatherWidget(cityId); // 使用新的城市ID更新天氣小部件
            updatePressureChart(apiKey); // 更新氣壓圖
        });
    }).catch(error => {
        console.error('獲取天氣數據時出錯:', error);
        alert('未找到該城市，請重新輸入');
    });
});
