import requests  # библиотека для запросов
import csv  # библиотека для записи данных в CSV формат
import time  # библиотека для работы с временем
import fake_useragent  # библиотека для работы с USER AGENT


def writer_csv_header():  # функция для создания заголовков во время записи в CSV
    with open('eonadzor.csv', 'w', encoding='utf-8') as file:  # записываем с кодировкой utf-8
        writer = csv.writer(file)
        writer.writerow((  # картэж(название) заголовков
            'ДАТА ПОЛУЧЕНИЯ',
            'НАИМЕНОВАНИЕ',
            'ЭКСПЛУАТИРУЮЩАЯ ОРГАНИЗАЦИЯ',
            'ЭКСПЕРТНАЯ ОРГАНИЗАЦИЯ',
            'РЕГ.НОМЕР',
            'ОБЪЕКТ ЭКСПЕРТИЗЫ',
            'НОМЕР УДОСТОВЕРЕНИЯ ЭКСПЕРТА',
            'ТЕРРИТОРИАЛЬНОЕ УПРАВЛЕНИЕ'))


def writer_csv(data):  # функция для записи данных в CSV файл
    with open('eonadzor.csv', 'a', encoding='utf-8') as f:  # записываем с кодировкой utf-8
        writer = csv.writer(f)
        writer.writerow([data['дата_получения'],  # ключи записываемых данных
                         data['наименование'],
                         data['эксплуатирующая организация'],
                         data['экспертная_организация'],
                         data['рег_номер'],
                         data['объект_экспертизы'],
                         data['номер_удостоверения_эксперта'],
                         data['территориальное_управление']])


def get_response(url):  # функция для получения данных
    fake_user_agent = fake_useragent.UserAgent().random  # использование библиотеки UserAgent
    headers = {'user-agent': fake_user_agent}  # создание заголовка для запроса
    response = requests.get(url, headers=headers)  # запрос по URL с параметрами заголовка

    response_json = response.json()  # получение данных в формате JSON
    return response_json  # возвращаем JSON в функцию


def get_json_items(json_items):  # функция для получение конкретных данных из JSON файла

    try:  # получение общего списка данных со страницы
        all_items = json_items["results"]
    except Exception as error:
        print(error)

    for item in all_items:  # цикл для получение данных из списка

        try:  # установка исключений и условий для непрерывного парсинга(при нормальной работе)
            # далее, ниже 7 конструкций, имеют аналогичную структуру и логику
            if item["reg_date"] == None:  # если данные отсутствуют, то записываем об этом
                date_reg = 'данные отсутствуют'
            else:  # в противном случае записываем эти данные
                date_reg = item["reg_date"].strip()
        except Exception as error:  # исключение для сбой работы
            print(error)  # выводим ошибку(исключение)
            date_reg = 'данные отсутствуют'  # и записываем об этом

        try:

            if item["name"] == None:
                name_project = 'данные отсутствуют'
            else:
                name_project = item["name"].strip()
        except Exception as error:
            print(error)
            name_project = 'данные отсутствуют'

        try:

            if item["operator"]["name"] == None:
                operating_organization = 'данные отсутствуют'
            else:
                operating_organization = item["operator"]["name"].strip()
        except Exception as error:
            print(error)
            operating_organization = 'данные отсутствуют'

        try:

            if item["expert"]["name"] == None:
                expert_organization = 'данные отсутствуют'
            else:
                expert_organization = item["expert"]["name"].strip()
        except Exception as error:
            print(error)
            expert_organization = 'данные отсутствуют'

        try:

            if item["reg_number"] == None:
                reg_number = 'данные отсутствуют'
            else:
                reg_number = item["reg_number"].strip()
        except Exception as error:
            print(error)
            reg_number = 'данные отсутствуют'

        try:

            if item["examination_object_source"] == None:
                examination_object_source = 'данные отсутствуют'
            else:
                examination_object_source = item["examination_object_source"].strip()
        except Exception as error:
            print(error)
            examination_object_source = 'данные отсутствуют'

        try:

            if item["expert_number"] == None:
                expert_reg_namber = 'данные отсутствуют'
            else:
                expert_reg_namber = item["expert_number"].strip()
        except Exception as error:
            print(error)
            expert_reg_namber = 'данные отсутствуют'

        try:

            if item["territorial_department"]["name"] == None:
                territorial_administration = 'данные отсутствуют'
            else:
                territorial_administration = item["territorial_department"]["name"].strip()
        except Exception as error:
            print(error)
            territorial_administration = 'данные отсутствуют'

        data = {  # список с о всеми данными
            'дата_получения': date_reg,
            'наименование': name_project,
            'эксплуатирующая организация': operating_organization,
            'экспертная_организация': expert_organization,
            'рег_номер': reg_number,
            'объект_экспертизы': examination_object_source,
            'номер_удостоверения_эксперта': expert_reg_namber,
            'территориальное_управление': territorial_administration
        }

        writer_csv(data)  # вызов функции и передаем список с данными в функцию для записи CSV файла


def main():  # функция для управления логикой кода

    writer_csv_header()  # вызов функции для создания заголовков

    for i in range(1, 500 + 1):  # цикл для отправки URL страницы для парсинга
        url = f'https://eo.nadzor-info.ru/api/expertise/?object_type=2&page={i}&pp=20&tag_glob=&year=2017%2C2022'

        get_json_items(get_response(url))  # вызов функции сбора данных, где аргумет функциия для получения данных у которой аргумент URL из цикла выши

        time.sleep(3)  # останновка всех процессов на 3 секунды
        print('собранно страниц', i)  # вывод результатов пользователю


if __name__ == '__main__':  # управляющия конструкция
    main()