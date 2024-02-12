import os

import telebot

from dotenv import load_dotenv


load_dotenv('.env')  # загружаем данные из виртуального окружения

bot_token = os.getenv('TELEGRAM_BOT_TOKEN')  # получаем токен бота

bot = telebot.TeleBot(bot_token)  # создаем бота


@bot.message_handler(commands=['start', 'help'])
def start_bot(message):
    """ Обработчик начальной команды бота """

    # отправляем в бот приветствие
    if message.text == '/start':

        bot.send_message(message.chat.id, 'Привет, {0.first_name}!'.format(message.from_user))
        bot.send_message(message.chat.id, 'Бот позволяет производить конвертацию валют\n'
                                          'USD, EUR, RUB по текущему курсу')

    # отправляем в бот список возможных команд
    if message.text == '/help':

        bot.send_message(message.chat.id, 'Основные команды бота\n'
                                          '/start - начало работы бота\n'
                                          '/help - вывод основных команд')


bot.polling(non_stop=True)  # команда запуска непрерывной работы бота
