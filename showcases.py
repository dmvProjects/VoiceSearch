import requests
import json
from addr import *

text = 'лед'

length = {'title': 30,
          'type': 10,
          'id': 10,
          'weight': 8
          }

engine = bert_showcases

data_raw = {"text": text,
            }

data_raw_json = json.dumps(data_raw, indent=2)


def showcases_search_request():
    r = requests.post(engine['addr'],
                      headers=engine['headers'],
                      data=data_raw_json,
                      timeout=25)
    print(f'Запрос:\n{r.request.url}\n'.replace('\'', '"'), text)

    if r.status_code != 200:
        print(r.status_code, r.text, r.headers)
        return False
    else:
        # print(r.json())
        result = r.json()['data']['showcases']

        if not result:
            print('NO RESULTS')
            return False

        print(f"Время выполнения запроса: {r.elapsed.total_seconds()}")
    # print(result)

    fields = [k for k, v in length.items() if v]
    field_format = ''
    for field in fields:
        field_format = field_format + '{:<' + str(length[field] + 4) + '}'
    fields_line = [str(field)[:length[field]] for field in fields]

    print(field_format.format(*fields_line))

    for showcase in result:
        print(
            f'\n{"-" * 45} {showcase["title"]} ({showcase["total"]}){"-" * 45}\n')
        for item in showcase['items']:
            # print(item)
            if item['type'] not in ('schedule',):
                asset = [str(item[field])[:length[field]] for field in fields]
            else:
                asset = [str(item['data'][field])[:length[field]] if field != 'weight' else str(item[field])[:length[field]] for field in fields ]
            print(field_format.format(*asset))


if __name__ == '__main__':
    showcases_search_request()
