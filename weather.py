import telebot
import datetime
import requests

bot = telebot.TeleBot('7518434190:AAE1AwGRjpXh1DW77tcKejW5EEW-Y7u9XsQ')

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
def get_weather(message):
    city = user_cities.get(message.chat.id)
    if not city:
        bot.send_message(message.chat.id, 'Вы еще не указали город. Нажмите на кнопку "Указать/изменить город", чтобы задать его.', reply_markup=main_menu())
        return
    try:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=2e1695f1a6ddc5a7d9cae7612b00ef7c'
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        #########################
        temperature = round(weather_data['main']['temp'] - 273.15, 1)
        wind_speed = weather_data['wind']['speed']
        #########################
        bot.send_message(message.chat.id, f'Погода в городе {city}: {temperature} градусов. Скорость ветра: {wind_speed} м/с.', reply_markup=main_menu())
        if temperature > 20:
            bot.send_message(message.chat.id, 'Сейчас очень жарко, наденьте легкую одежду.')
        elif temperature > 15:
            bot.send_message(message.chat.id, 'Сейчас тепло, наденьте что-нибудь легкое.')
        elif temperature > 0:
            bot.send_message(message.chat.id, 'Сейчас прохладно, наденьте что-то теплое.')
        else:
            bot.send_message(message.chat.id, 'Сейчас холодно, наденьте теплую куртку и шапку.')
            
    except requests.exceptions.HTTPError as e:
        bot.send_message(message.chat.id, f'Произошла ошибка при запросе погоды: {e}', reply_markup=main_menu())
    except KeyError as e:
        bot.send_message(message.chat.id, f'Произошла ошибка при обработке ответа от сервера: {e}', reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла неизвестная ошибка: {e}', reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text == 'Подробно')
def get_weather(message):
    city = user_cities.get(message.chat.id)
    cs = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Дождь \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F32B',
    }
    if not city:
        bot.send_message(message.chat.id, 'Вы еще не указали город. Нажмите на кнопку "Указать/изменить город", чтобы задать его.', reply_markup=main_menu())
        return
    try:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=d62e5f3282f85b0d26fab128e9e94fdb'
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        #########################
        temperature = round(weather_data['main']['temp'] - 273.15, 1)
        wind_speed = weather_data['wind']['speed']
        humidity = weather_data['main']['humidity']
        pressure = weather_data['main']['pressure']
        sunrise_timestamp = datetime.datetime.fromtimestamp(weather_data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(weather_data['sys']['sunset'])
        visibility = weather_data['visibility']
        wname = weather_data['weather'][0]['main']
        if wname in cs:
            desk = cs[wname]
        else:
            desk = 'Не пойму что на улице.'
        #########################
        bot.send_message(message.chat.id, f'Погода в городе {city}: {desk}\n'
                                          f'Температура: {temperature} градусов.\n'
                                          f'Скорость ветра: {wind_speed} м/с.\n'
                                          f'Влажность: {humidity}%.\n'
                                          f'Давление: {pressure} мм ртутного столба\n'
                                          f'Видимость: {visibility} метров\n'
                                          f'Восход: {sunrise_timestamp} по МСК\n'
                                          f'Закат: {sunset_timestamp} по МСК', reply_markup=main_menu())
            
    except requests.exceptions.HTTPError as e:
        bot.send_message(message.chat.id, f'Произошла ошибка при запросе погоды: {e}', reply_markup=main_menu())
    except KeyError as e:
        bot.send_message(message.chat.id, f'Произошла ошибка при обработке ответа от сервера: {e}', reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла неизвестная ошибка: {e}', reply_markup=main_menu())

bot.polling()
