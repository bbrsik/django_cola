import requests
import datetime
import os
from django.core.exceptions import ObjectDoesNotExist
from weather.models import Weather
from django.utils import timezone
from user.models import Profile


def should_update_weather(location='Saint Petersburg') -> bool:
    try:
        last_update = Weather.objects.filter(location=location).latest('created_at')
    except ObjectDoesNotExist:
        return True
    current_time = timezone.now()
    difference = current_time - last_update.created_at
    max_difference = datetime.timedelta(hours=1)
    return difference >= max_difference


def request_weather_data(location='Saint Petersburg'):
    # todo вынести в настройки
    key = os.getenv("WEATHER_API_KEY")
    WEATHER_URL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{0}/today/?key={1}'
    url = WEATHER_URL.format(location, key)
    response = requests.get(url, timeout=2)
    data = response.json()
    weather_data = {
        'location': data.get('address'),
        'description': data.get('days')[0].get('description'),
        'temperature': convert_fahrenheit_to_celsius(data.get('currentConditions').get('temp'))
    }
    return weather_data


def convert_fahrenheit_to_celsius(temperature_fahrenheit):
    return round((temperature_fahrenheit - 32) / 1.8)
