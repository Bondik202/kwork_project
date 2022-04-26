import requests  # библиотека для HTTP запросов
from data_api_vk import TOKEN, V, URL  # импортируем настройки
import time  # библиотека для работы со временем
import csv  # библиотека для работы с CSV файлами


# функция записи данных в csv файл
def writer_csv(data):
    with open('user_list_status.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([data['name'],
                         data['link_user'],
                         data['status']])


# функция получения метаданных юзеров
def get_name(user_link, id_user):
     response = requests.get(URL + 'users.get', params={
         'access_token': TOKEN,  # секретный токен
         'v': V,  # версия VK API
         'user_ids': id_user  # id юзера
     })
     response_json = response.json()  # ответ от запроса в формате json

     try:  # исключение для нормального сценария
         status = response_json['response'][0]['is_closed']  # статус страницы юзера
         if status == False:  # условие где False = открытой странице

             first_name = response_json['response'][0]['first_name']  # имя юзера
             last_name = response_json['response'][0]['last_name']  # фамилия юзера
             name = first_name + ' ' + last_name  # Имя и фамилия юзера
             link_user = user_link  # ссылка на страницу юзера
             status = 'Доступ к странице ОТКРЫТ'  # переменная со статусом доступа к странице юзера

             data = {  # словарь со всеми данными
                 'name': name,
                 'link_user': link_user,
                 'status': status
             }

             writer_csv(data)  # передаем данные в функцию
             print(data)  # для контроля исполнения скрипта

         elif status == True:  # условие где True = закрытой страницей

             first_name = response_json['response'][0]['first_name']  # имя юзера
             last_name = response_json['response'][0]['last_name']  # фамилия юзера
             name = first_name + ' ' + last_name  # Имя и фамилия юзера
             link_user = user_link  # ссылка на страницу юзера
             status = 'Доступ к странице ЗАКРЫТ'  # переменная со статусом доступа к странице юзера

             data = {  # словарь со всеми данными
                 'name': name,
                 'link_user': link_user,
                 'status': status
             }

             writer_csv(data)  # передаем данные в функцию
             print(data)  # для контроля исполнения скрипта

     except Exception as error:  # исключение для ошибки
         print(error)  # вывод ошибки


# функция получение юзеров сообщества
def get_user(count_offset):
    # метод возвращает список участников сообщества
    response = requests.get(URL + 'groups.getMembers', params={
        'access_token': TOKEN,  # секретный токен
        'v': V,  # версия VK API
        'group_id': 'ognestrelny_mir',  # идентификатор или короткое имя сообщества
        'offset': count_offset  # смещение, необходимое для выборки определенного подмножества участников. По умолчанию 0
    })

    response_json = response.json()  # ответ от запроса в формате json
    list_item = response_json['response']['items']  # общий список юзеров с смещением offset

    # цикл для извлечения (получения) и форматирования ссылки на страницу юзера
    for i in list_item:
        id_user = i  # получения ID пользователя
        user_link = 'https://vk.com/id' + str(id_user)  # получения ссылки на страницу юзера
        get_name(user_link, id_user)  # направляем данные в функцию получения метаданных юзеров
        time.sleep(1)


# глвная функция
def main():
    count_offset = 0  # счётчик смещения
    for i in range(5):  # цикл для назначение смещения юзеров, одна этерация = 1000 смещением юзеров
        get_user(count_offset)  # пересылаем смещение в функцию получение юзеров сообщества
        count_offset += 1000  # добавляем смещение


# конструкция запуска
if __name__ == '__main__':
    main()