from data_api_vk import OWNER_ID, TOKEN, V, DOMAIN, COUNT, URL, ALBUM_ID, ALBUM_IDS  # импортируем настройки
import requests  # библиотека для HTTP запросов
import time  # библиотека для работы со временем
import re  # библиотека для работы с регулярными выражениями
import csv  # библиотека для записи данных в формат CSV
import datetime  # библиотека для работы с ТАЙМСТАМПОМ


def writer_csv(data):  # функция записи данных в CSV формат

    with open('data_user.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([data['user-link'],
                         data['link_comment_photos'],
                         data['name_user'],
                         data['name_produkt'],
                         data['price_rub'],
                         data['data_time']])


# функция для получения методанных о юзере
def get_meta_data_user(data_time, user_id, comment_text_link_id, link_comment_photos, user_link):
    # Этот метод для работы с данными пользователей
    response_user = requests.get(URL + 'users.get', params={
        'user_ids': user_id,  # идентификаторы пользователей
        'access_token': TOKEN,  # секретный токен
        'v': V  # версия VK API
    })
    response_user_json = response_user.json()  # масив от запроса в формате json

    first_name = response_user_json['response'][0]['first_name']  # получаем Имя
    last_name = response_user_json['response'][0]['last_name']  # получаем Фамилию
    name_user = last_name + ' ' + first_name  # Имя и Фамилия

    time.sleep(1)  # задержка на 1 секунду

    get_general_data_collection(comment_text_link_id, name_user, data_time, link_comment_photos, user_link)  # пересылаем данные в функцию


# функци для получение цены продукты его названия, а так же компоновки и подготовке всех данных на запись
def get_general_data_collection(comment_text_link_id, name_user, data_time, link_comment_photos, user_link):
    # Этот метод возвращает список фотографий в альбоме
    response_get_photos = requests.get(URL + 'photos.get', params={
        'owner_id': OWNER_ID,  # идентификатор владельца альбома
        'access_token': TOKEN,  # секретный токен
        'v': V,  # версия VK API
        'count': 1, # количество записей, которое будет получено
        'album_id': ALBUM_ID,  # идентификатор альбома
        'photo_ids': comment_text_link_id # идентификаторы фотографий, информацию о которых необходимо вернуть
    })

    response_json_get_photos = response_get_photos.json()  # получаем ответ от запроса в JSON формате
    text_photos = response_json_get_photos['response']['items'][0]['text'] # # получаем общий текст под фотографией (описание продукта)


    name_produkt = text_photos[:text_photos.find('\n'):]  # получаем название продукта
    price_rub_spisok = re.findall(r'[-+]?\d+ руб', text_photos)  # получаем цену (str) списком

    try:  # если цена в описании присудствует то:
        price_rub = price_rub_spisok[0]  # распоковываем список с ценой
        price_rub_str = price_rub.split(' ')  # сплитуем по пробелу
        price_rub_int = price_rub_str[0]  # получаем первый элемент в цене (второй будет "руб")
        price_rub_int = int(price_rub_int)  # получаем цену (int) числом
    except:  # если ценны нет в описании то:
        price_rub_int = 'цены на странице нет'  # записываем в переменную "цены на странице нет"

    data = {
        'user-link': user_link,  # ссылка на страницу юзера
        'link_comment_photos': link_comment_photos,  # ссылка на коментарий оставленный юзером
        'name_user': name_user,  # Имя и Фамилия юзера
        'name_produkt': name_produkt,  # Название продукта
        'price_rub': price_rub_int,  # Цена продукта
        'data_time': data_time  # время и дата коментария
    }
    print(data)  # для визуального просмотра данных
    writer_csv(data)  # отправляем данные на запись в функцию


# главная функция
def main():
    # метод для получения метаданых всех коментариев(под конкретным альбомом, или под указыными в params)
    response_all_comments = requests.get(URL + 'photos.getAllComments', params={
        'owner_id': OWNER_ID,  # идентификатор пользователя или сообщества, которому принадлежат фотографии
        'access_token': TOKEN,  # секретный токен
        'v': V,  # версия VK API
        'count': 100,  # количество комментариев, которое необходимо получить
        'album_id': ALBUM_ID  # идентификатор альбома, если идентификатор не указан то получаем данные всех альбомов)
    })

    response_all_comments_json = response_all_comments.json()  # получения общего масива (метаданных комнтариеев) на запрос, в формате JSON
    all_response = response_all_comments_json['response']['items']  # переходим к масиву методанных коментрарие

    time.sleep(1) # устанавлеваем задержку на 1 секунду

    for i in all_response:  # запускаем цикл для прохода по масиву методанных коментареев
        user_id = i['from_id']  # получае ID юзера оставившего коментарий
        time_stamp = i['date']  # получаем тайм стамп
        data_time = datetime.datetime.fromtimestamp(time_stamp) # конвентируем тайм стамп в дату
        comment_text_link_id = i['pid']  # получаем ID фотографии где юзер оставил коментарий
        link_comment_photos = 'https://vk.com/photo-17557338_' + str(comment_text_link_id) # ссылка на фотографию с оставленным комментарием юзера
        user_link = 'https://vk.com/id' + str(user_id)  # ссылка на страницу юзера

        time.sleep(1)  # устанавлеваем задержку на 1 секунду

        get_meta_data_user(data_time, user_id, comment_text_link_id, link_comment_photos, user_link)  # пересылаем данные в функцию


if __name__ == '__main__':  # конструкция для запуска
    main()