document.getElementById('search-button').addEventListener('click', function() {
    const city = document.getElementById('city-input').value;
    if (city) {
        fetchWeatherData(city);
    }
});

document.getElementById('toggle-light').addEventListener('click', function() {
    document.body.classList.toggle('dark-mode');
});

function fetchWeatherData(city) {
    const apiKey = 'YOUR_API_KEY';
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            document.getElementById('city-name').textContent = data.name;
            document.getElementById('temperature').textContent = data.main.temp;
            document.getElementById('humidity').textContent = data.main.humidity;
            
            
            document.getElementById('weather-forecast').src = 'URL_TO_WEATHER_FORECAST_IMAGE';
            document.getElementById('pressure-chart').src = 'URL_TO_PRESSURE_CHART_IMAGE';
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
        });
}
