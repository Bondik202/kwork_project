import httpx
import csv


def writer_csv_header():  # функция создания заголовков
    with open('eonadzor.csv', 'w', encoding='utf-8') as file:  # записываем с кодировкой utf-8
        writer = csv.writer(file)
        writer.writerow((
            'Название эксплуатирующей организации',
            'ИНН',
            'Генеральный директор',
            'Юридический адрес',
            'Телефон',
            'URL',
            'Количество проведенных экспертиз по ЗС (2017 г.)',
            'Количество проведенных экспертиз по ЗС (2018 г.)',
            'Количество проведенных экспертиз по ЗС (2019 г.)',
            'Количество проведенных экспертиз по ЗС (2020 г.)',
            'Количество проведенных экспертиз по ЗС (2021 г.)',
            'Количество проведенных экспертиз по ЗС (2022 г.)'
            ))


def writer_csv(data):  # функция записи данных
    with open('eonadzor.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([data['name_company'],
                         data['inn_company'],
                         data['name_director'],
                         data['your_address'],
                         data['phone'],
                         data['url'],
                         data['count_2017'],
                         data['count_2018'],
                         data['count_2019'],
                         data['count_2020'],
                         data['count_2021'],
                         data['count_2022']
                         ])


def get_json(url):  # создание запроса к API
    response = httpx.get(url)
    response_json = response.json()
    return response_json


def get_item_company(json_response):  # парсинг полученых JSON обьектов
    count_organization = 0  # счетчик организаций
    all_items = json_response["results"]  # парсинг всех данных

    for item in all_items:  # цикл збора данных

        try:  # получение id компаний
            id_company = item["id"]
        except:
            id_company = 'данные отсутствуют'

        try:  # получение имени организации
            name_company = item["name"]
        except:
            name_company = 'данные отсутствуют'

        try:  # получение ИНН организации
            inn_company = item["inn"]
        except:
            inn_company = 'данные отсутствуют'

        try:  # получение данных директора организации
            name_director = item["director"]
        except:
            name_director = 'данные отсутствуют'

        try:  # получение юр. адреса организации
            your_address = item["address"]
        except:
            your_address = 'данные отсутствуют'

        try:  # парсинг данных проведенных экспертиз
            charts_all = item["charts"]["by_month"]

            for charts in charts_all:
                counts_2017 = 0
                counts_2018 = 0
                counts_2019 = 0
                counts_2020 = 0
                counts_2021 = 0
                counts_2022 = 0

                if charts["value"] == '2017-01-01' or charts["value"] == '2017-02-01' or charts["value"] == '2017-03-01' or charts["value"] == '2017-04-01' or charts["value"] == '2017-05-01' or charts["value"] == '2017-06-01' or charts["value"] == '2017-07-01' or charts["value"] == '2017-08-01' or charts["value"] == '2017-09-01' or charts["value"] == '2017-10-01' or charts["value"] == '2017-11-01' or charts["value"] == '2017-12-01':
                    counts_2017 = counts_2017 + charts["count"]
                    counts_2018 = ''
                    counts_2019 = ''
                    counts_2020 = ''
                    counts_2021 = ''
                    counts_2022 = ''

                elif charts["value"] == '2018-01-01' or charts["value"] == '2018-02-01' or charts["value"] =='2018-03-01' or charts["value"] == '2018-04-01' or charts["value"] == '2018-05-01' or charts["value"] == '2018-06-01' or charts["value"] == '2018-07-01' or charts["value"] == '2018-08-01' or charts["value"] == '2018-09-01' or charts["value"] == '2018-10-01' or charts["value"] == '2018-11-01' or charts["value"] == '2018-12-01':
                    counts_2018 = counts_2018 + charts["count"]
                    counts_2017 = ''
                    counts_2019 = ''
                    counts_2020 = ''
                    counts_2021 = ''
                    counts_2022 = ''

                elif charts["value"] == '2019-01-01' or charts["value"] == '201902-01' or charts["value"] == '2019-03-01' or charts["value"] == '2019-04-01' or charts["value"] == '2019-05-01' or charts["value"] == '2019-06-01' or charts["value"] == '2019-07-01' or charts["value"] == '2019-08-01' or charts["value"] == '2019-09-01' or charts["value"] == '2019-10-01' or charts["value"] == '2019-11-01' or charts["value"] == '2019-12-01':
                    counts_2019 = counts_2019 + charts["count"]
                    counts_2018 = ''
                    counts_2017 = ''
                    counts_2020 = ''
                    counts_2021 = ''
                    counts_2022 = ''

                elif charts["value"] == '2020-01-01' or charts["value"] == '2020-02-01' or charts["value"] == '2020-03-01' or charts["value"] == '2020-04-01' or charts["value"] == '2020-05-01' or charts["value"] == '2020-06-01' or charts["value"] == '2020-07-01' or charts["value"] == '2020-08-01' or charts["value"] == '2020-09-01' or charts["value"] == '2020-10-01' or charts["value"] == '2020-11-01' or charts["value"] == '2020-12-01':
                    counts_2020 = counts_2020 + charts["count"]
                    counts_2018 = ''
                    counts_2019 = ''
                    counts_2017 = ''
                    counts_2021 = ''
                    counts_2022 = ''

                elif charts["value"] == '2021-01-01' or charts["value"] == '2021-02-01' or charts["value"] == '2021-03-01' or charts["value"] == '2021-04-01' or charts["value"] == '2021-05-01' or charts["value"] == '2021-06-01' or charts["value"] == '2021-07-01' or charts["value"] == '2021-08-01' or charts["value"] == '2021-09-01' or charts["value"] == '2021-10-01' or charts["value"] == '2021-11-01' or charts["value"] == '2021-12-01':
                    counts_2021 = counts_2021 + charts["count"]
                    counts_2018 = ''
                    counts_2019 = ''
                    counts_2020 = ''
                    counts_2017 = ''
                    counts_2022 = ''

                elif charts["value"] == '2022-01-01' or charts["value"] == '2022-02-01' or charts["value"] == '2022-03-01' or charts["value"] == '2022-04-01' or charts["value"] == '2022-05-01' or charts["value"] == '2022-06-01' or charts["value"] == '2022-07-01' or charts["value"] == '2022-08-01' or charts["value"] == '2022-09-01' or charts["value"] == '2022-10-01' or charts["value"] == '2022-11-01' or charts["value"] == '2022-12-01':
                    counts_2022 = counts_2022 + charts["count"]
                    counts_2018 = ''
                    counts_2019 = ''
                    counts_2020 = ''
                    counts_2021 = ''
                    counts_2017 = ''

                count_2017 = counts_2017
                count_2018 = counts_2018
                count_2019 = counts_2019
                count_2020 = counts_2020
                count_2021 = counts_2021
                count_2022 = counts_2022
        except AttributeError:
            continue
        #  запрос для получения телефонов ораганизации
        url = f'https://eo.nadzor-info.ru/api/epb-eo/organization/{id_company}/show_phone/'
        response = httpx.get(url)
        response_json = response.json()

        try:  # получение телефонов
            all_phones = response_json["phones"]
            phone = ",".join(map(str, all_phones))
        except:
            phone = 'данные отсутствуют'

        try:  # получение ссылки на организацию
            url_organozation = f'https://eo.nadzor-info.ru/organization/{id_company}'
        except:
            url_organozation = 'данные отсутствуют'
        # запись получиных данных в словарь
        data = {
            'name_company': name_company,
            'inn_company': inn_company,
            'name_director': name_director,
            'your_address': your_address,
            'phone': phone,
            'url': url_organozation,
            'count_2017': count_2017,
            'count_2018': count_2018,
            'count_2019': count_2019,
            'count_2020': count_2020,
            'count_2021': count_2021,
            'count_2022': count_2022
            }

        count_organization += 1
        writer_csv(data)
        print('Ожидайте, происходит сбор данных с организаций......', f'Собранно и записанно данных в CSV файл с {count_organization} организаций ', sep = '\n')

def main():  # управляющая функция

    writer_csv_header()

    year_list = ['2017', '2018', '2019', '2020', '2021', '2022']  # список с годами проведенных экспертиз

    for year in year_list:  # цикл для формирования URL
        url = f'https://eo.nadzor-info.ru/api/epb-eo/organization/?&object_type=2&page=1&pp=1000&year={year}%2C{year}'

        print(f'Происходит сбор и формирование данных за {year} год, Ожидайте.....')
        get_item_company(get_json(url))


if __name__ == '__main__':  # управляющая конструкция
    main()