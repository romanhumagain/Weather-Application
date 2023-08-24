from django.shortcuts import render
import datetime
import requests
import os
# Create your views here.

def fetch_weather_data(city):
  """Fetch weather data for the given city using OpenWeatherMap API."""
  WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')
  url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}'
  parameters = {'units':'metric'}
  
  response = requests.get(url , parameters)
  
  if response.status_code != 200:
    return None
  return response.json()

def home(request):
    context = {}
    if request.method == "POST":
        city = request.POST.get('city').strip().lower()
        data = fetch_weather_data(city)

        if data:
            weather_data = data.get('weather', [{}])[0]
            main_data = data.get('main', {})
            
            context['description'] = weather_data.get('description', 'N/A')
            context['icon'] = weather_data.get('icon', 'N/A')
            context['temp'] = main_data.get('temp', 'N/A')
            context['day'] = datetime.date.today()
            context['city'] = city.capitalize()
            
            # Check if rain is expected
            if 'rain' in data:
                rain_data = data.get('rain', {})
                rain_volume = rain_data.get('1h', 0)  # this checks for rain volume in the last 1 hour
                if rain_volume > 0:
                    context['rain_notification'] = f"Rain expected! Volume: {rain_volume}mm in the last hour."
        else:
            context['error'] = 'Unable to fetch weather data or city not recognized.'
    
    return render(request, 'weatherapp/index.html', context)
