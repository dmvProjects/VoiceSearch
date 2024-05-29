import requests
import json
from addr import *

text = 'лед'

length = {'title': 30,
          'type': 10,
          'id': 10,
          'weight': 8
          }

TOKEN = 'eyJkYXRhIjoie1wiZXhwaXJlc1wiOjE3MTgzNDkzOTEsXCJsaWZlc3BhblwiOjI1OTIwMDAsXCJwcmluY2lwYWxcIjp7XCJmcmVlbWl1bVwiOjAsXCJleHRpZFwiOlwibWFjOkFBOkJCOkNDOkREOjM4OjE1XCIsXCJzdWJzY3JpYmVyXCI6e1wiZ3JvdXBzXCI6W3tcImlkXCI6MzUwMTcsXCJleHRpZFwiOlwiZXI6ZG9tYWluOnNwYlwifV0sXCJleHRpZFwiOlwic3BiOjc4MDAyNzg0NDUxMVwiLFwic3Vic2NyaWJlcl90eXBlXCI6XCJCMkNcIixcImlzX2d1ZXN0XCI6ZmFsc2UsXCJ0eXBlXCI6XCJzdWJzY3JpYmVyXCIsXCJpZFwiOjM3MzE0NTA4fSxcInBsYXRmb3JtXCI6e1wib3BlcmF0b3JcIjp7XCJ0aXRsZVwiOlwiXCIsXCJpZFwiOjIsXCJleHRpZFwiOlwiZXJcIn0sXCJ0aXRsZVwiOlwiXCIsXCJpZFwiOjExOSxcImV4dGlkXCI6XCJhbmRyb2lkdHZfc3RiXCJ9LFwiZ3JvdXBzXCI6W3tcImlkXCI6MzQxOTcsXCJleHRpZFwiOlwiZXI6ZXZlcnlvbmVcIn1dLFwib3BlcmF0b3JcIjp7XCJ0aXRsZVwiOlwiXCIsXCJpZFwiOjIsXCJleHRpZFwiOlwiZXJcIn0sXCJ0eXBlXCI6XCJkZXZpY2VcIixcImlkXCI6OTA0Mjk5NDJ9fSIsInNpZ25hdHVyZSI6IjBQZmx0TTErZzd0UkNGV3NPZ1Y3cDFNT3hYMDlpWkU3cisxVjMyZXphL3M9In0='

engine = {'addr': 'http://158.160.48.107/pages/search',
                  'headers': {'Content-Type': 'application/json',
                              'X-Auth-Token': TOKEN,
                              },
                  'ranker': '',
                  'threshold_1': 10,
                  'threshold_2': 50
                  }


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
