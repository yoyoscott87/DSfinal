function kelvinToCelsius(kelvin) {
    return kelvin - 273.15;
}

document.getElementById("autoControlBtn").addEventListener("click", function() {
    // 發送GET請求到Flask應用程序
    fetch("/auto")
        .then(response => response.json())
        .then(data => {
            // 在控制台中打印回應
            console.log(data);

            // 更新溫度和濕度
            document.getElementById("temperature").innerText = data.temperature ? `${data.temperature} °C` : "N/A";
            document.getElementById("humidity").innerText = data.humidity ? `${data.humidity} %` : "N/A";

            // 更新冷氣和除濕機狀態
            document.getElementById("air-conditioner").innerText = data.air_conditioner;
            document.getElementById("dehumidifier").innerText = data.dehumidifier;
        })
        .catch(error => {
            console.error('Error:', error);
        });
});

document.getElementById("toggleAirConditionerBtn").addEventListener("click", function() {
    const currentStatus = document.getElementById("air-conditioner").innerText;

    fetch("/toggle_air_conditioner", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ current_status: currentStatus })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            document.getElementById("air-conditioner").innerText = data.new_status;
        } else {
            console.error('Error:', data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

document.getElementById("toggleDehumidifierBtn").addEventListener("click", function() {
    const currentStatus = document.getElementById("dehumidifier").innerText;

    fetch("/toggle_hum", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ current_status: currentStatus })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            document.getElementById("dehumidifier").innerText = data.new_status;
        } else {
            console.error('Error:', data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

document.getElementById('search-button').addEventListener('click', function() {
    var city = document.getElementById('city-input').value;
    searchWeather(city);
    loadWeatherWidget(city);
});

function searchWeather(city) {
    fetch('/weather', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ city: city })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('weather').textContent = data.weather_description;
        document.getElementById('loctemperature').textContent = data.temperature ? `${data.temperature} °C` : "N/A";
        document.getElementById('lochumidity').textContent = data.humidity ? `${data.humidity} %` : "N/A";
        document.getElementById('air').textContent = data.air;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function loadWeatherWidget(city) {
    const cityNameToId = {
        "東京": "1850147",
        "新北": "1675151",
        "台中": "1668399",
        "大阪": "1853909",
        "紐約": "5128581",
        "北京": "1816670",
        "倫敦": "2643743",
        "巴黎": "2988507",
        "台北": "1668341",
        "台南": "1668355",
        "上海": "1796236",
        "洛杉磯": "5368361",
        "高雄": "1673820",
        "花蓮": "1674502",
        "桃園": "1667905",
        "南投": "1671564"
    };

    // 獲取對應的城市ID
    var cityId = cityNameToId[city];
    if (!cityId) {
        alert('無法找到對應的城市ID');
        return;
    }

    // 清除之前的插件內容
    document.getElementById('openweathermap-widget-11').innerHTML = '';

    // 動態加載天氣預報圖插件
    window.myWidgetParam ? window.myWidgetParam : window.myWidgetParam = [];
    window.myWidgetParam.push({
        id: 11,
        cityid: cityId,
        appid: 'b55132e7d0d008aa945b18e4cd2f5a02',
        units: 'metric',
        containerid: 'openweathermap-widget-11',
    });

    (function() {
        var script = document.createElement('script');
        script.async = true;
        script.charset = "utf-8";
        script.src = "//openweathermap.org/themes/openweathermap/assets/vendor/owm/js/weather-widget-generator.js";
        var s = document.getElementsByTagName('script')[0];
        s.parentNode.insertBefore(script, s);
    })();
}

// AI
$(document).ready(function() {
    $('#question-form').submit(function(event) {
        event.preventDefault();
        var question = $('#question').val();
        $.ajax({
            type: 'POST',
            url: '/ask',
            data: {question: question},
            success: function(response) {
                $('#chat-box').append('<p style="font-size: 20px;"><strong>你:</strong> ' + question + '</p>');
                $('#chat-box').append('<p style="font-size: 20px;"><strong>管家:</strong> ' + response.answer + '</p>');

            }
        });
    });
});
