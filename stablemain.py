TELEGRAM_TOKEN = '7518434190:AAE1AwGRjpXh1DW77tcKejW5EEW-Y7u9XsQ'
WEATHER_API_KEY = '277f6801b8e46543933b08ed8b36c7ae'

import requests
import datetime
import telebot
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


from handlers import bot

if __name__ == '__main__':
    bot.polling(none_stop=True)

from weather import get_weather_data, format_weather_simple, format_weather_detailed
from config import TELEGRAM_TOKEN

bot = telebot.TeleBot(TELEGRAM_TOKEN)
user_cities = {}

def main_menu():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Погода', 'Указать/изменить город', 'Подробно')
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я бот, который может показывать погоду. Чтобы узнать погоду, нужно указать город, для этого используйте "Указать/изменить город".', reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text == 'Указать/изменить город')
def change_city(message):
    bot.send_message(message.chat.id, 'Напишите название города, который ты хочешь установить.', reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, set_city)

def set_city(message):
    city = message.text
    user_cities[message.chat.id] = city
    bot.send_message(message.chat.id, f'Я запомнил город {city}.', reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text == 'Погода')
def send_weather_simple(message):
    city = user_cities.get(message.chat.id)
    if not city:
        bot.send_message(message.chat.id, 'Вы еще не указали город. Нажмите на кнопку "Указать/изменить город", чтобы задать его.', reply_markup=main_menu())
        return

    try:
        weather_data = get_weather_data(city)
        bot.send_message(message.chat.id, format_weather_simple(weather_data, city), reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {e}', reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text == 'Подробно')
def send_weather_detailed(message):
    city = user_cities.get(message.chat.id)
    if not city:
        bot.send_message(message.chat.id, 'Вы еще не указали город. Нажмите на кнопку "Указать/изменить город", чтобы задать его.', reply_markup=main_menu())
        return

    try:
        weather_data = get_weather_data(city)
        bot.send_message(message.chat.id, format_weather_detailed(weather_data, city), reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {e}', reply_markup=main_menu())


bot.polling()
