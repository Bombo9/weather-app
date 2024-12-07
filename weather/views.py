import requests
from django.shortcuts import render
from django.http import HttpResponse

# Define your OpenWeather API key here
API_KEY = 'eca28905d57e23240078801b24556de1'  # Replace with your actual OpenWeather API key


# Helper functions
def clothing_recommendations(temp, weather_condition):
    if temp < 10:
        return "Wear a heavy coat, scarf, and gloves."
    elif 10 <= temp < 20:
        return "Wear a light jacket or sweater."
    elif weather_condition in ["rain", "drizzle"]:
        return "Carry an umbrella or wear a waterproof jacket."
    elif temp >= 30:
        return "Wear light and breathable fabrics like cotton."
    else:
        return "Dress comfortably for mild weather."


def energy_saving_tips(temp):
    if temp < 10:
        return "Consider using a programmable thermostat to efficiently heat your home."
    elif 10 <= temp < 20:
        return "Use natural sunlight during the day to warm your space."
    elif temp >= 30:
        return "Close curtains during peak sunlight hours to keep your home cool."
    else:
        return "Turn off heating or cooling systems when not needed."


def get_lat_lon(city_name):
    """
    Fetch the latitude and longitude for the given city using OpenWeather's Geocoding API.
    """
    geocoding_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}"
    response = requests.get(geocoding_url)
    data = response.json()

    if response.status_code == 200:
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        return lat, lon
    else:
        return None, None  # Return None if the city is not found or the request fails


# Views
def index(request):
    weather = None
    if request.method == "POST":
        city = request.POST.get('city')
        lat, lon = get_lat_lon(city)  # Get latitude and longitude for the city
        if lat and lon:  # Proceed only if valid lat/lon are returned
            url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()

            temp = data['main']['temp']
            weather_condition = data['weather'][0]['description']
            clothing_tip = clothing_recommendations(temp, weather_condition)
            energy_tip = energy_saving_tips(temp)

            weather = {
                'city': city,
                'temperature': temp,
                'description': weather_condition,
                'icon': data['weather'][0]['icon'],
                'clothing_tip': clothing_tip,
                'energy_tip': energy_tip,
            }
        else:
            weather = {'error': "City not found or invalid. Please try again."}

    return render(request, 'weather/index.html', {'weather': weather})


def forecast(request):
    forecast_data = None
    if request.method == "POST":
        city = request.POST.get('city')
        lat, lon = get_lat_lon(city)  # Get latitude and longitude for the city
        if lat and lon:  # Proceed only if valid lat/lon are returned
            url = f"http://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&appid={API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()

            forecast_data = []
            for day in data['daily']:
                day_weather = {
                    'date': day['dt'],
                    'temperature': day['temp']['day'],
                    'weather': day['weather'][0]['description'],
                    'icon': day['weather'][0]['icon']
                }
                forecast_data.append(day_weather)
        else:
            forecast_data = {'error': "City not found or invalid. Please try again."}

    return render(request, 'weather/forecast.html', {'forecast_data': forecast_data})


def alerts(request):
    alert_data = None
    if request.method == "POST":
        city = request.POST.get('city')
        lat, lon = get_lat_lon(city)  # Get latitude and longitude for the city
        if lat and lon:  # Proceed only if valid lat/lon are returned
            url = f"http://api.openweathermap.org/data/2.5/alerts?lat={lat}&lon={lon}&appid={API_KEY}"
            response = requests.get(url)
            data = response.json()

            if 'alerts' in data:
                alert_data = data['alerts']
            else:
                alert_data = "No weather alerts for this location."
        else:
            alert_data = {'error': "City not found or invalid. Please try again."}

    return render(request, 'weather/alert.html', {'alert_data': alert_data})


def schedule_task(request):
    if request.method == 'GET':
        # Logic for GET requests
        return render(request, 'weather/schedule.html')
    elif request.method == 'POST':
        # Logic for POST requests (if needed)
        return HttpResponse("POST request received.")
    else:
        return HttpResponse("Method not allowed", status=405)
