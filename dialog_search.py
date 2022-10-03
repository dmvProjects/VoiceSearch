import requests
from addr import *
import json


text = 'найди голубой щенок'

data_raw = {"clientId": "ivan",
            "query": text,
            "data": {
                     "token": TOKEN,
                     "context": {
                                 "isOperatorAppForeground": 'true',
                                 "volume": 3,
                                 "foregroundActivityName": "SearchResultActivit",
                                 "foregroundAppPackageName": "com.ertelecom.voiceassistant"
                                }
                    }
            }

data_raw_json = json.dumps(data_raw, indent=2)


def dialog_searh_request():
    r = requests.post(just_ai['addr'],
                      headers=just_ai['headers'],
                      json=data_raw,
                      timeout=25)
    if r.status_code != 200:
        print(r.status_code, r.text, r.headers)
        return False
    else:
        # print(r.json())
        result = r.json()
    return result


reply = dialog_searh_request()
# print(reply)
if reply['data']['replies'][0]['method'] == 'OpenContent':
    print(f'Карточка "{reply["data"]["replies"][0]["body"]}"')
elif reply['data']['replies'][0]['method'] == 'OpenSearchView':
    print(f'Поиск "{reply["data"]["replies"][0]["body"]["params"]["text"]}"')
