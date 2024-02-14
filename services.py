import json
import os

import pytz
import requests
import datetime
import random


def get_currencies_course():
    """ Получает данные о текущем курсе валют """

    # формируем адрес запроса
    url_api = 'https://www.cbr-xml-daily.ru/daily_json.js'

    req = requests.get(url_api)  # Посылаем запрос

    if req.status_code == 200:  # проверяем на корректность ответа

        data_in = req.content.decode()  # Декодируем ответ, чтобы Кириллица отображалась корректно
        req.close()  # закрываем сеанс запроса

        data_out = json.loads(data_in)  # преобразуем полученные данные из формата json
        writing_json(data_out)  # записываем полученные данные в файл

        return True

    if req.status_code != 200:
        return False


def writing_json(currencies_data):
    """ Записывает данные в формате json """

    # путь к файлу, в котором хранятся курсы валют
    file_data = os.path.abspath(f'./currencies_course.json')

    with open(file_data, 'w', encoding='utf-8') as file:
        json.dump(currencies_data, file, sort_keys=False, indent=4, ensure_ascii=False)


def reading_json():
    """ Считывает данные из формата json """

    # путь к файлу, в котором хранятся курсы валют
    file_data = os.path.abspath(f'./currencies_course.json')

    try:
        with open(file_data, 'r', encoding='utf-8') as file:
            data_list = json.load(file)
        return data_list
    except FileNotFoundError:
        print('Файла пока не существует, будет создан новый файл')
        data_list = []
        return data_list


def check_currencies_course_date():
    """ Проверяет актуальность данных в сохраненном файле """

    currencies_dict = reading_json()  # получаем список курсов валют из файла
    currencies_date = currencies_dict['Date']  # получаем дату курса валют в файле

    # определяем разницу в днях между текущей датой и датой курса валют
    days_difference = get_days_difference(currencies_date)

    # если сохраненный курс валют был получен день или более назад
    if days_difference >= 1:
        fresh_currencies_course = get_currencies_course()  # получаем свежий курс валют

        return fresh_currencies_course

    else:
        return True


def get_days_difference(date_time):
    """ Считает разницу между текущей датой и полученной датой в днях """

    desired_timezone = pytz.timezone('Europe/Moscow')  # устанавливаем часовой пояс
    date_time_now = datetime.datetime.now()  # получаем текущие дату и время

    time_now = date_time_now.astimezone(desired_timezone)  # текущее время с учетом часового пояса
    # преобразуем время в формате ISO полученное из файла с учетом часового пояса
    time_received = datetime.datetime.fromisoformat(date_time).astimezone(desired_timezone)

    # считаем разницу между текущей датой и полученной датой в днях
    days_difference = (time_now.date() - time_received.date()).days

    return days_difference


def prepare_datas(data_in):
    """ Подготовка данных для конвертации """

    sum_to_convert = int(data_in[1])  # получаем сумму для конвертации

    convert_type = ' '.join(data_in[2:]).lower()  # получаем тип конвертации

    # конвертируем валюту
    converted_data = converting_currencies(sum_to_convert, convert_type)

    return converted_data


def converting_currencies(sum_to_convert, convert_type):
    """ Конвертация валюты """

    currencies_data = reading_json()  # получаем данные о валютах

    usd_course = currencies_data['Valute']['USD']['Value']  # курс доллара по отношению к рублю
    eur_course = currencies_data['Valute']['EUR']['Value']  # курс евро по отношению к рублю

    # конвертация рублей в доллары
    if convert_type == 'rub to usd':
        sum_after_convert = round((sum_to_convert / usd_course), 2)
        return f'{sum_after_convert} USD'

    # конвертация рублей в евро
    if convert_type == 'rub to eur':
        sum_after_convert = round((sum_to_convert / eur_course), 2)
        return f'{sum_after_convert} EUR'

    # конвертация долларов в евро
    if convert_type == 'usd to eur':
        sum_after_convert = round((sum_to_convert * (usd_course / eur_course)), 2)
        return f'{sum_after_convert} EUR'

    # конвертация евро в доллары
    if convert_type == 'eur to usd':
        sum_after_convert = round((sum_to_convert * (eur_course / usd_course)), 2)
        return f'{sum_after_convert} USD'


def check_word(user_word):
    """ Проверяет слово, введенное пользователем """

    hello_words = ['приветули', 'здравствуй', 'хай', 'здорово']
    bye_words = ['пока', 'покеда', 'прощай', 'до свидания', 'увидимся']

    for word in hello_words:
        result = word.find(user_word)
        if result >= 0:
            hello_answer = random.choice(hello_words)
            return hello_answer
            break

    for word in bye_words:
        result = word.find(user_word)
        if result >= 0:
            bye_answer = random.choice(bye_words)
            return bye_answer
            break


# print(check_word('пок'))
