    // Allow Enter key to trigger search
        document.getElementById('cityInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                getWeather();
            }
        });

        async function getWeather() {
            const cityInput = document.getElementById('cityInput');
            const cityName = cityInput.value.trim();
            
            if (!cityName) {
                showError('Please enter a city name');
                return;
            }

            // Show loading state
            showLoading(true);
            hideError();
            hideWeatherInfo();

            try {
                
                const response = await fetch(`/weather?city=${encodeURIComponent(cityName)}`);
                const data = await response.json();

                if (data.error) {
                    showError(data.error);
                } else {
                    displayWeather(data);
                }
            } catch (error) {
                showError('Failed to fetch weather data. Please try again.');
                console.error('Error:', error);
            } finally {
                showLoading(false);
            }
        }

        function displayWeather(data) {
            document.getElementById('cityName').textContent = data.city;
            document.getElementById('temperature').textContent = Math.round(data.temperature) + '°C';
            document.getElementById('description').textContent = data.description;
            document.getElementById('humidity').textContent = data.humidity + '%';
            document.getElementById('windSpeed').textContent = data.wind_speed + ' m/s';
            
          
            const iconUrl = `https://openweathermap.org/img/wn/${data.icon}@2x.png`;
            document.getElementById('weatherIcon').src = iconUrl;
            
            showWeatherInfo();
        }

        function showWeatherInfo() {
            document.getElementById('weatherInfo').classList.add('show');
        }

        function hideWeatherInfo() {
            document.getElementById('weatherInfo').classList.remove('show');
        }

        function showError(message) {
            const errorDiv = document.getElementById('error');
            errorDiv.textContent = message;
            errorDiv.classList.add('show');
        }

        function hideError() {
            document.getElementById('error').classList.remove('show');
        }

        function showLoading(show) {
            const loadingDiv = document.getElementById('loading');
            if (show) {
                loadingDiv.classList.add('show');
            } else {
                loadingDiv.classList.remove('show');
            }
        }