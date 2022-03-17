import json
import requests

TOKEN = 'eyJkYXRhIjoie1wiZXhwaXJlc1wiOjE2NDg3MzAyNTIsXCJsaWZlc3BhblwiOjI1OTIwMDAsXCJwcmluY2lwYWxcIjp7XCJmcmVlbWl1bVwiOjAsXCJleHRpZFwiOlwibWFjOjExOjIyOjMzOjQ0OjU5OjY2XCIsXCJzdWJzY3JpYmVyXCI6e1wiZ3JvdXBzXCI6W3tcImlkXCI6MzUwMzcsXCJleHRpZFwiOlwiZXI6ZG9tYWluOnBlcm1cIn1dLFwiZXh0aWRcIjpcInBlcm06NTkwMDE4NTA1MTY2XCIsXCJzdWJzY3JpYmVyX3R5cGVcIjpcIkIyQ1wiLFwiaXNfZ3Vlc3RcIjpmYWxzZSxcInR5cGVcIjpcInN1YnNjcmliZXJcIixcImlkXCI6ODEzMjM3NjV9LFwicGxhdGZvcm1cIjp7XCJvcGVyYXRvclwiOntcInRpdGxlXCI6XCJcIixcImlkXCI6MixcImV4dGlkXCI6XCJlclwifSxcInRpdGxlXCI6XCJcIixcImlkXCI6NDQsXCJleHRpZFwiOlwiYW5kcm9pZF9pcHR2XCJ9LFwiYXR0cnNcIjpudWxsLFwiZ3JvdXBzXCI6W3tcImlkXCI6MzQxOTcsXCJleHRpZFwiOlwiZXI6ZXZlcnlvbmVcIn1dLFwib3BlcmF0b3JcIjp7XCJ0aXRsZVwiOlwiXCIsXCJpZFwiOjIsXCJleHRpZFwiOlwiZXJcIn0sXCJ0eXBlXCI6XCJkZXZpY2VcIixcImlkXCI6OTA0MjIzMDV9fSIsInNpZ25hdHVyZSI6InhHODlnbm1USGtIbk90RGJmdGhaeHlpUGd3Y2l1aDJUU0hCVlwvc3dPWklnPSJ9'

# Вводные для поиска вбивать в этот словарь. Если значения у ключа не True, то оно игнорируется
template = {'text': 'Игра',  # string
            'title': '',  # string
            # 'types': ['movie', 'serial', 'schedule', 'subscription', 'channel', 'channel_package', 'program', 'live_tv_show'],  # movie, serial, schedule, subscription, channel, channel_package, program, live_tv_show
            'types': [],
            'countryNames': [],  # string
            'countryIds': [],  # integer
            'ageRating': '',  # R0, R6, R12, R16, R18
            'adultState': '',  # NOT_ADULT, ADULT
            'kinopoiskRatingFrom': 0,  # float 0..10
            'kinopoiskRatingTo': 0,  # float 0..10
            'imdbRatingFrom': 0,  # float 0..10
            'imdbRatingTo': 0,  # float 0..10
            'quality': '',  # SD, HD, 4K
            'startDt': '',  # date 2022-03-05
            'genre': '',  # string
            'genreId': 0,  # integer
            'persons': [],  # string
            'releasedAtFrom': '',  # date 2022-03-05
            'releasedAtTo': '',  # date 2022-03-05
            'limit': 300,  # integer 1..1000, default 10
            'page': 0,  # integer 1.., default 1
            'sortBy': '',  # isHd, kinopoiskrating, imdbrating, weight; default: weight
            'sortDirection': '',  # ASC, DESC; default: DESC
            'ranker': ''  # proximity_bm25, bm25, none, wordcount, proximity, matchany, fieldmask, sph04, expr; default: sph04
            }

# Тут задается длина выводимой строки для каждого поля, ячейка обрезается до этого значения,
# закомментированные поля и поля с значением 0 не выводятся. Порядок вывода = порядок перечисления.
lenght = {'title': 40,
          'type': 10,
          'id': 10,
          'weight': 8,
          'dif': 5,
          'genres': 40,
          'imdbRating': 6,
          'kinopoiskRating': 6,
          'rating': 6,
          'adult': 9,
          'description': 2000}

THRESHOLD_1 = 12
THRESHOLD_2 = 50


def search_api_request():
    # Забираем только заполненные поля из вводных для формирования запроса
    request_body = {}
    for k, v in template.items():
        if v:
            request_body[k] = v

    # Формируем и выполняем запрос
    print(f'Запрос:\n{request_body}\n'.replace('\'', '"'))
    request_body_json = json.dumps(request_body, indent=2)
    r = requests.post('http://testasr.rd.ertelecom.ru/search',
                      headers={'Content-Type': 'application/json',
                               'accept': 'application/json',
                               'X-Auth-Token': TOKEN,
                               },
                      data=request_body_json,
                      timeout=1)
    if r.status_code != 200:
        print(r.status_code, r.text, r.headers)
    else:
        # Проверяем полученный ответ на наличие результатов
        result = r.json()['items']
        if not result:
            print('NO RESULTS')
            return False
        print(f"Всего результатов: {r.json()['total']}\n")

        # Формируем список полей, которые нужно вывести, форматируем по длине, выводим заголовок таблицы
        fields = [k for k, v in lenght.items() if v]
        field_format = ''
        for field in fields:
            field_format = field_format + '{:<' + str(lenght[field] + 4) + '}'
        fields_line = [str(field)[:lenght[field]] for field in fields]
        print(field_format.format(*fields_line), '\n')

        # определяем вес первого результата как максимум для расчета разницы остальных относительно него и расстановки трешхолдов
        if template['page'] <= 1:
            top_weight = result[0]['weight']
        # если был запрос не страницы 1, перезапрашиваем первую и берем вес верхнего результата
        else:
            request_body_top = request_body
            request_body_top['limit'] = 1
            request_body_top['page'] = 1
            request_body_top['sortDirection'] = 'DESC'
            request_body_top_json = json.dumps(request_body_top, indent=2)
            r_top = requests.post('http://testasr.rd.ertelecom.ru/search',
                              headers={'Content-Type': 'application/json',
                                       'accept': 'application/json',
                                       'X-Auth-Token': TOKEN,
                                       },
                              data=request_body_top_json,
                              timeout=1)
            top_weight = r_top.json()['items'][0]['weight']
            # result_with_dif = r_top.json()['items'] + result_with_dif  # можно добавить к выводу первый результат с первой страницы для страниц >2

        # Обработка и вывод всех ассетов из ответа
        thd_1 = False  # статусы трешхолдов выводились/не выводились
        thd_2 = False
        # расчет разницы веса ассета относительно максимального
        for item in result:
            dif = int((1 - item["weight"] / top_weight) * 100)
            if item["weight"] == top_weight:
                item['dif'] = '0%'
            else:
                item['dif'] = f'-{dif}%'
            # вывод строк трешхолдов на границах весов
            if not thd_1 and dif >= THRESHOLD_1:
                print(f'\n-------------------------------------------- Threshold_1 -{THRESHOLD_1}% --------------------------------------------\n')
                thd_1 = True
            if not thd_2 and dif >= THRESHOLD_2:
                print(f'\n******************************************** Threshold_2 -{THRESHOLD_2}% ********************************************\n')
                thd_2 = True
            # очистка описания от мусорных литералов
            if 'description' in item.keys():
                item['description'] = item['description'].replace('\n', ' ').replace('\r', ' ')
            # приведение к описанному формату и длине строк и вывод
            asset = [str(item[field])[:lenght[field]] for field in fields]
            print(field_format.format(*asset))
        # вывод строки с первым трешхолдом под таблицей, если все ассеты попали выше первого трешхолда
        if not thd_1:
            print(f'\n-------------------------------------------- Threshold 1 -{THRESHOLD_1}% --------------------------------------------\n')


if __name__ == '__main__':
    search_api_request()
