# Работа с погодой через API
import requests
import datetime
from config import WEATHER_API_KEY

def get_weather_data(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def format_weather_simple(weather_data, city):
    temperature = round(weather_data['main']['temp'] - 273.15, 1)
    wind_speed = weather_data['wind']['speed']
    return f'Погода в городе {city}: {temperature} градусов. Скорость ветра: {wind_speed} м/с.'

def format_weather_detailed(weather_data, city):
    cs = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Дождь \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F32B',
    }

    temperature = round(weather_data['main']['temp'] - 273.15, 1)
    wind_speed = weather_data['wind']['speed']
    humidity = weather_data['main']['humidity']
    pressure = weather_data['main']['pressure']
    sunrise_timestamp = datetime.datetime.fromtimestamp(weather_data['sys']['sunrise'])
    sunset_timestamp = datetime.datetime.fromtimestamp(weather_data['sys']['sunset'])
    visibility = weather_data['visibility']
    wname = weather_data['weather'][0]['main']
    desk = cs.get(wname, 'Не пойму что на улице.')
    
    return (f'Погода в городе {city}: {desk}\n'
            f'Температура: {temperature} градусов.\n'
            f'Скорость ветра: {wind_speed} м/с.\n'
            f'Влажность: {humidity}%.\n'
            f'Давление: {pressure} мм ртутного столба\n'
            f'Видимость: {visibility} метров\n'
            f'Восход: {sunrise_timestamp} по МСК\n'
            f'Закат: {sunset_timestamp} по МСК')
