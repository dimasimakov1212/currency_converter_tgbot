import json
import os

import requests


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

    if req.status_code != 200:
        print("В настоящий момент сервис недоступен. Попробуйте позже.")


def writing_json(currencies_data):
    """ Записывает данные в формате json """

    # путь к файлу, в котором хранятся курсы валют
    file_data = os.path.abspath(f'./currencies_course.json')

    with open(file_data, 'w', encoding='utf-8') as file:
        json.dump(currencies_data, file, sort_keys=False, indent=4, ensure_ascii=False)


# get_currencies_course()
