import requests
from addr import *
import json

text = 'лед'

engine = bert_suggests

# Вводные для поиска вбивать в этот словарь. Если значения у ключа не True, то оно игнорируется
template = {'text': text,  # string
            'title': '',  # string
            # 'types': ['movie', 'serial', 'schedule', 'subscription', 'channel', 'program'],  # movie, serial, schedule, subscription, channel, channel_package, program, live_tv_show
            'types': ["movie", "serial", "schedule", "channel", "channel-package", "subscription"],
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
            'limit': 1000,  # integer 1..1000, default 10
            'page': 0,  # integer 1.., default 1
            'sortBy': '',  # isHd, kinopoiskrating, imdbrating, weight; default: weight
            'sortDirection': '',  # ASC, DESC; default: DESC
            # 'ranker': engine['ranker']
            }

lenght = {'title': 30,
          'type': 10,
          # 'id': 10,
          # 'weight': 8,
          # 'dif': 5,
          # 'genres': 20,
          # 'imdbRating': 6,
          # 'kinopoiskRating': 6,
          # 'rating': 6,
          # 'adult': 9,
          # 'description': 2000
          }


# data_raw = {"text": text,
#             }
#
# data_raw_json = json.dumps(data_raw, indent=2)


def suggests_search_request():
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
    # print(f'Запрос:\n{r.request.url}\n'.replace('\'', '"'))
    # print(r.status_code)
    if r.status_code != 200:
        print(r.status_code, r.text, r.headers)
        return False
    else:
        result = r.json()['items']

    if not result:
        print('NO RESULTS')
        return False

    print(f"Время выполнения запроса: {r.elapsed.total_seconds()}\n")
    # print(f"Всего результатов: {r.json()['total']}\n")


    # Формируем список полей, которые нужно вывести, форматируем по длине, выводим заголовок таблицы
    fields = [k for k, v in lenght.items() if v]
    field_format = ''
    for field in fields:
        field_format = field_format + '{:<' + str(lenght[field] + 4) + '}'
    fields_line = [str(field)[:lenght[field]] for field in fields]
    print(field_format.format(*fields_line), '\n')

    top_weight = result[0]['weight']
    done = []
    i = 0
    for item in result:
        if [item['title'], item['type']] not in done and i < 10:
            item['adult'] = item['adult']['type']
            # расчет разницы веса ассета относительно максимального
            dif = int((1 - item["weight"] / top_weight) * 100)
            if item["weight"] == top_weight:
                item['dif'] = 'MAX'
            else:
                item['dif'] = f'-{dif}%'
            # очистка описания от ломающих верстку литералов
            if 'description' in item.keys():
                item['description'] = item['description'].replace('\n', ' ').replace('\r', ' ')
            # приведение к описанному формату и длине строк и вывод
            asset = [str(item[field])[:lenght[field]] for field in fields]
            print(field_format.format(*asset))
            done.append([item['title'], item['type']])
            i += 1

if __name__ == '__main__':
    suggests_search_request()
