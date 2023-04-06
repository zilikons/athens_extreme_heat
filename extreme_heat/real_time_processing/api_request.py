import os
import datetime
import pandas as pd
import requests
import time

API_KEY = os.environ.get('WEATHER_API_KEY')
LATITUDE = os.environ.get('LATITUDE')
LONGITUDE = os.environ.get('LONGITUDE')

BASE_URL = 'http://api.openweathermap.org/data/2.5/forecast'
PARAMS = {'lat': LATITUDE, 'lon': LONGITUDE, 'appid': API_KEY, 'units': 'metric'}
def convert_epoch_to_gmt3(epoch_time):
    gmt_offset = 3 * 60 * 60
    gmt_time = epoch_time + gmt_offset
    formatted_time = pd.to_datetime(int(gmt_time),unit='s')
    return formatted_time

def weather_data_to_pandas():
    results = requests.get(BASE_URL, params=PARAMS).json()['list']
    current_time = pd.to_datetime(datetime.datetime.now())
    dates = []
    temperature = []
    apparent_temperature = []
    humidity = []
    wind_speed = []
    for result in results:
        dates.append(convert_epoch_to_gmt3(result['dt']))
        temperature.append(result['main']['temp'])
        apparent_temperature.append(result['main']['feels_like'])
        humidity.append(result['main']['humidity'])
        wind_speed.append(result['wind']['speed'])
    data = pd.DataFrame({'date': dates, 'temperature': temperature, 'apparent_temperature': apparent_temperature, 'humidity': humidity, 'wind_speed': wind_speed})
    data['day'] = data['date'].dt.day
    data['hour'] = data['date'].dt.hour
    data['month'] = data['date'].dt.month
    return (data, current_time)
