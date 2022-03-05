import json
import requests

token = 'eyJkYXRhIjoie1wiZXhwaXJlc1wiOjE2NDg3MzAyNTIsXCJsaWZlc3BhblwiOjI1OTIwMDAsXCJwcmluY2lwYWxcIjp7XCJmcmVlbWl1bVwiOjAsXCJleHRpZFwiOlwibWFjOjExOjIyOjMzOjQ0OjU5OjY2XCIsXCJzdWJzY3JpYmVyXCI6e1wiZ3JvdXBzXCI6W3tcImlkXCI6MzUwMzcsXCJleHRpZFwiOlwiZXI6ZG9tYWluOnBlcm1cIn1dLFwiZXh0aWRcIjpcInBlcm06NTkwMDE4NTA1MTY2XCIsXCJzdWJzY3JpYmVyX3R5cGVcIjpcIkIyQ1wiLFwiaXNfZ3Vlc3RcIjpmYWxzZSxcInR5cGVcIjpcInN1YnNjcmliZXJcIixcImlkXCI6ODEzMjM3NjV9LFwicGxhdGZvcm1cIjp7XCJvcGVyYXRvclwiOntcInRpdGxlXCI6XCJcIixcImlkXCI6MixcImV4dGlkXCI6XCJlclwifSxcInRpdGxlXCI6XCJcIixcImlkXCI6NDQsXCJleHRpZFwiOlwiYW5kcm9pZF9pcHR2XCJ9LFwiYXR0cnNcIjpudWxsLFwiZ3JvdXBzXCI6W3tcImlkXCI6MzQxOTcsXCJleHRpZFwiOlwiZXI6ZXZlcnlvbmVcIn1dLFwib3BlcmF0b3JcIjp7XCJ0aXRsZVwiOlwiXCIsXCJpZFwiOjIsXCJleHRpZFwiOlwiZXJcIn0sXCJ0eXBlXCI6XCJkZXZpY2VcIixcImlkXCI6OTA0MjIzMDV9fSIsInNpZ25hdHVyZSI6InhHODlnbm1USGtIbk90RGJmdGhaeHlpUGd3Y2l1aDJUU0hCVlwvc3dPWklnPSJ9'


# Вводняе для поиска вбивать в этот словарь. Если значения в поле не True, то оно игнорируется
template = {'text': 'СТС',  # string
            'title': '',  # string
            'types': [],  # movie, serial, schedule, subscription, channel, channel_package
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
            'limit': 0,  # integer 1..20, default 10
            'page': 0,  # integer 1.., default 1
            'sortBy': '',  # isHd, kinopoiskrating, imdbrating, weight; default: weight
            'sortDirection': '',  # ASC, DESC; default: DESC
            'ranker': ''  # proximity_bm25, bm25, none, wordcount, proximity, matchany, fieldmask, sph04, expr; default: sph04
            }

# тут задается длина выводимой строки для каждого поля, обрезается до этого значения
lenght = {'title': 40,
          'weight': 8,
          'dif': 5,
          'type': 10,
          'imdbRating': 6,
          'kinopoiskRating': 6,
          'rating': 6,
          'adult': 9,
          'genres': 40,
          'description': 1000}


def search_api_request(**kwargs):
    request_body = {}
    for k, v in template.items():
        if v:
            request_body[k] = v
    print('Вводные')
    for k, v in request_body.items():
        print(f'{k}: {v}')
    print('')
    request_body = json.dumps(request_body, indent=2)
    r = requests.post('http://testasr.rd.ertelecom.ru/search',
                      headers={'Content-Type': 'application/json',
                               'accept': 'application/json',
                               'X-Auth-Token': token,
                               },
                      data=request_body,
                      timeout=1)
    if r.status_code != 200:
        print(r.status_code, r.text, r.headers)
    else:
        fields = ['title', 'weight', 'dif']
        additional = [k for k, v in kwargs.items() if v]
        if additional:
            for field in additional:
                fields.append(field)
        field_format = ''
        for field in fields:
            field_format = field_format + '{:<' + str(lenght[field] + 4) + '}'
        fields_line = [str(field)[:lenght[field]] for field in fields]
        print(field_format.format(*fields_line), '\n')
        result_with_dif = r.json()['items']
        top_weight = result_with_dif[0]['weight']
        for item in result_with_dif:
            if item["weight"] == top_weight:
                item['dif'] = '0%'
            else:
                item['dif'] = f'-{int((1 - item["weight"] / top_weight) * 100)}%'
            result = [str(item[field])[:lenght[field]] for field in fields]
            print(field_format.format(*result))


if __name__ == '__main__':
    search_api_request(type=True,
                       imdbRating=True,
                       kinopoiskRating=True,
                       rating=True,
                       adult=True,
                       genres=True,
                       description=True)
