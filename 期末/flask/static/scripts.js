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
        document.getElementById('loctemperature').textContent = data.temperature;
        document.getElementById('lochumidity').textContent = data.humidity;
        document.getElementById('air').textContent = data.air;
        
    })
    .catch(error => {
        console.error('Error:', error);
    });
}








//AI
$(document).ready(function() {
    $('#question-form').submit(function(event) {
        event.preventDefault();
        var question = $('#question').val();
        $.ajax({
            type: 'POST',
            url: '/ask',
            data: {question: question},
            success: function(response) {
                $('#chat-box').append('<p><strong>You:</strong> ' + question + '</p>');
                $('#chat-box').append('<p><strong>Bot:</strong> ' + response.answer + '</p>');
            }
        });
    });
});
