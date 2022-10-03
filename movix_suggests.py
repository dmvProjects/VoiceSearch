import json
import requests
from addr import *

# text = 'новости'

lenght = {'title': 30,
          'type': 10,
          # 'id': 10,
          # 'description': 2000
          }

engine = movix_suggests


def movix_searh_request():
    r = requests.get(engine['addr'],
                     headers=engine['headers'],
                     params={'text': text},
                     timeout=25)
    print(f'Запрос:\n{text}\n')

    if r.status_code != 200:
        print(r.status_code, r.text, r.headers)
        return False
    else:
        # Проверяем полученный ответ на наличие результатов
        result = r.json()['data']['items']

        if not result:
            print('NO RESULTS')
            return False
        print(f"Время выполнения запроса: {r.elapsed.total_seconds()}\n")
        # print(f"Всего результатов: {r.json()['data']['total']}\n")

        fields = [k for k, v in lenght.items() if v]
        field_format = ''
        for field in fields:
            field_format = field_format + '{:<' + str(lenght[field] + 4) + '}'
        fields_line = [str(field)[:lenght[field]] for field in fields]
        print(field_format.format(*fields_line), '\n')

        for item in result:
            asset = [str(item['data'][field])[:lenght[field]] for field in fields]
            print(field_format.format(*asset))


if __name__ == '__main__':
    movix_searh_request()
