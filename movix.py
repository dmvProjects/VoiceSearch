import json
import requests
from addr import *


text = 'друг'


engine = movix
r = requests.get(engine['addr'],
                 headers=engine['headers'],
                 params={'text': text},
                 timeout=25)

data = r.json()['data']['showcases']

# for i in range(len(data)):
#     print(i)
#     for k, v in data[i].items():
#         print(k, v)

showcase = data[0]['items']
for i in range(len(showcase)):
    print(i)
    for k, v in showcase[i].items():
        print(k, v)
