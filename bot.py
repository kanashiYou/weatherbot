# Отвечает за запуск бота
from handlers import bot

if __name__ == '__main__':
    bot.polling(none_stop=True)
