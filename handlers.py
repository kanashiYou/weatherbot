# Обработчики команд
import telebot
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
