import json
import requests
from addr import *

text = 'Лед'

engine = bert_showcases
# engine = sergey_bert_matnicore

mode = 'list'    # showcases, list

# Вводные для поиска вбивать в этот словарь. Если значения у ключа не True, то оно игнорируется
template = {'text': text,  # string
            'title': '',  # string
            # 'types': ['movie', 'serial', 'schedule', 'subscription', 'channel', 'program'],  # movie, serial, schedule, subscription, channel, channel_package, program, live_tv_show
            'types': [],
            'countryNames': [],  # string
            'countryIds': [],  # integer
            'ageRating': '',  # R0, R6, R12, R16, R18
            'adultState': '',  # "type": "not-adult", "type": "adult"
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
            'limit': 0,  # integer 1..1000, default 10
            'page': 0,  # integer 1.., default 1
            'sortBy': '',  # isHd, kinopoiskrating, imdbrating, weight; default: weight
            'sortDirection': '',  # ASC, DESC; default: DESC
            'ranker': engine['ranker']
            }

# Тут задается длина выводимой строки для каждого поля, ячейка обрезается до этого значения,
# закомментированные поля и поля с значением 0 не выводятся. Порядок вывода = порядок перечисления.
lenght = {'title': 30,
          'type': 10,
          'id': 10,
          'weight': 8,
          'dif': 5,
          'genres': 20,
          'imdbRating': 6,
          'kinopoiskRating': 6,
          'rating': 6,
          'adult': 9,
          'description': 2000
          }

if mode == 'showcases':
    lenght = {'title': 30,
              'type': 10,
              'id': 10,
              'weight': 8,
              'dif': 5,
              # 'genres': 20,
              # 'imdbRating': 6,
              # 'kinopoiskRating': 6,
              # 'rating': 6,
              # 'adult': 9,
              'description': 2000
              }

THRESHOLD_1 = engine['threshold_1']
THRESHOLD_2 = engine['threshold_2']


def search_api_request(mode='showcases'):
    # Забираем только заполненные поля из вводных для формирования запроса
    request_body = {}
    for k, v in template.items():
        if v:
            request_body[k] = v

    # Формируем и выполняем запрос
    print(f'Запрос:\n{request_body}\n'.replace('\'', '"'))
    request_body_json = json.dumps(request_body, indent=2)
    r = requests.post(engine['addr'],
                      headers=engine['headers'],
                      data=request_body_json,
                      timeout=25)
    if r.status_code != 200:
        print(r.status_code, r.text, r.headers)
    else:
        # Проверяем полученный ответ на наличие результатов
        # print(r.json())
        result = r.json()['items']

        if not result:
            print('NO RESULTS')
            return False
        print(f"Время выполнения запроса: {r.elapsed.total_seconds()}")
        print(f"Всего результатов: {r.json()['total']}\n")

        # Формируем список полей, которые нужно вывести, форматируем по длине, выводим заголовок таблицы
        fields = [k for k, v in lenght.items() if v]
        field_format = ''
        for field in fields:
            field_format = field_format + '{:<' + str(lenght[field] + 4) + '}'
        fields_line = [str(field)[:lenght[field]] for field in fields]
        print(field_format.format(*fields_line), '\n')

        # определяем вес первого результата как максимум для расчета разницы остальных относительно него и расстановки трешолдов
        if template['page'] <= 1:
            top_weight = result[0]['weight']
        # если был запрос не страницы 1, перезапрашиваем первую и сохраняем в переменную вес верхнего результата
        else:
            request_body_top = request_body
            request_body_top['limit'] = 1
            request_body_top['page'] = 1
            request_body_top['sortDirection'] = 'DESC'
            request_body_top_json = json.dumps(request_body_top, indent=2)
            r_top = requests.post(engine['addr'],
                                  headers=engine['headers'],
                                  data=request_body_top_json,
                                  timeout=25)
            top_weight = r_top.json()['items'][0]['weight']
            # result_with_dif = r_top.json()['items'] + result_with_dif  # можно добавить к выводу первый результат с первой страницы для страниц >2

        if mode == 'list':
            # Обработка и вывод всех ассетов из ответа
            thd_1 = False  # статусы трешолдов выводились/не выводились
            thd_2 = False

            for item in result:
                item['adult'] = item['adult']['type']
                # расчет разницы веса ассета относительно максимального
                dif = int((1 - item["weight"] / top_weight) * 100)
                if item["weight"] == top_weight:
                    item['dif'] = 'MAX'
                else:
                    item['dif'] = f'-{dif}%'
                # вывод строк трешолдов на границах весов
                if not thd_1 and dif >= THRESHOLD_1:
                    print(f'\n-------------------------------------------- Threshold_1 -{THRESHOLD_1}% --------------------------------------------\n')
                    thd_1 = True
                if not thd_2 and dif >= THRESHOLD_2:
                    print(f'\n******************************************** Threshold_2 -{THRESHOLD_2}% ********************************************\n')
                    thd_2 = True
                # очистка описания от ломающих верстку литералов
                if 'description' in item.keys():
                    item['description'] = item['description'].replace('\n', ' ').replace('\r', ' ')
                # приведение к описанному формату и длине строк и вывод
                asset = [str(item[field])[:lenght[field]] for field in fields]
                print(field_format.format(*asset))
            # вывод строки с первым трешолдом под таблицей, если все ассеты попали выше первого трешолда
            if not thd_1:
                print(f'\n-------------------------------------------- Threshold 1 -{THRESHOLD_1}% --------------------------------------------\n')

        elif mode == 'showcases':
            showcases = {}
            for item in result:
                if engine == vanya:
                    item['adult'] = item['adult']['type']

                dif = int((1 - item["weight"] / top_weight) * 100)
                if item["weight"] == top_weight:
                    item['dif'] = 'MAX'
                else:
                    item['dif'] = f'-{dif}%'

                if 'description' in item.keys():
                    item['description'] = item['description'].replace('\n', ' ').replace('\r', ' ')

                # if item['type'] not in showcases.keys():
                #     asset = [str(item[field])[:lenght[field]] for field in fields]
                #     asset_str = field_format.format(*asset) + '\n'
                #     showcases[item['type']] = asset_str
                # else:
                #     asset = [str(item[field])[:lenght[field]] for field in fields]
                #     asset_str = field_format.format(*asset) + '\n'
                #     showcases[item['type']] += asset_str
                if item['type'] not in showcases.keys():
                    showcases[item['type']] = []
                asset = [str(item[field])[:lenght[field]] for field in fields]
                asset_str = field_format.format(*asset) + '\n'
                showcases[item['type']].append(asset_str)
            # print(showcases)
            genres = {'movie': 'Фильмы',
                      'serial': 'Сериалы',
                      'program': 'Телевидение',
                      'channel': 'Недавние передачи',
                      'live-tv-show': 'Фильмы'}
            for k, v in showcases.items():
                print(f'\n-------------------------------------------- {k} ({len(v)})--------------------------------------------\n')
                print(''.join(v))


if __name__ == '__main__':
    search_api_request(mode=mode)

