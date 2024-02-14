import os

import telebot

from dotenv import load_dotenv

from services import check_currencies_course_date, prepare_datas, check_word, writing_log

load_dotenv('.env')  # загружаем данные из виртуального окружения

bot_token = os.getenv('TELEGRAM_BOT_TOKEN')  # получаем токен бота

bot = telebot.TeleBot(bot_token)  # создаем бота


@bot.message_handler(commands=['start', 'help'])
def start_bot(message):
    """ Обработчик начальных команд бота """

    # отправляем в бот приветствие
    if message.text == '/start':

        bot.send_message(message.chat.id, 'Привет, {0.first_name}!'.format(message.from_user))
        bot.send_message(message.chat.id, 'Бот позволяет производить конвертацию валют\n'
                                          'USD, EUR, RUB по текущему курсу\n'
                                          'Для получения дополнительной информации выберите команду\n'
                                          '/help')

        # проверяем актуальность сохраненных данных о курсе валют
        # если данные устарели, то они будут обновлены
        checking = check_currencies_course_date()

        if checking:
            bot.send_message(message.chat.id, 'Данные курсов валют обновлены')

        else:
            bot.send_message(message.chat.id, 'В настоящий момент невозможно получить'
                                              ' свежий курс валют')

    # отправляем в бот список возможных команд
    if message.text == '/help':

        bot.send_message(message.chat.id, 'Основные команды бота\n'
                                          '/start - начало работы бота\n'
                                          '/help - вывод основных команд\n'
                                          '/convert - конвертация валют\n'
                                          '--------- Пример запроса на конвертацию ---------\n'
                                          '/convert 100 EUR to USD\n'
                                          'выведет результат конвертации 100 евро в доллары США')

    # записываем действия пользователя в лог файл
    writing_log(message.text, message.chat.id)


@bot.message_handler(commands=['convert'])
def converter(message):
    """ Обработчик команды конвертации валюты """

    user_text = message.text  # сохраняем сообщение от пользователя
    data_list = user_text.split()  # преобразуем строку в список

    # проверяем правильность введенного пользователем запроса
    if len(data_list) == 5:

        # если запрос правильный производим конвертацию валюты
        converted_data = prepare_datas(data_list)

        bot.send_message(message.chat.id, f'Результат - {converted_data}')

    else:
        bot.send_message(message.chat.id, 'Вероятно вы неправильно ввели запрос\n'
                                          'Попробуйте еще раз')

    # записываем действия пользователя в лог файл
    writing_log(message.text, message.chat.id)


@bot.message_handler(content_types=['text'])
def communicate_to_user(message):
    """ Обработчик сообщений от пользователя """

    user_message = message.text.lower()  # сохраняем сообщение от пользователя

    bot_answer = check_word(user_message)  # проверяем слово пользователя и получаем ответ
    bot.send_message(message.chat.id, bot_answer)  # отправляем ответ пользователю

    # записываем действия пользователя в лог файл
    writing_log(message.text, message.chat.id)


bot.polling(non_stop=True)  # команда запуска непрерывной работы бота
