TOKEN = 'eyJkYXRhIjoie1wiZXhwaXJlc1wiOjE2NTQ0MTczOTcsXCJsaWZlc3BhblwiOjI1OTIwMDAsXCJwcmluY2lwYWxcIjp7XCJmcmVlbWl1bVwiOjAsXCJkZXZpY2VfZ3JvdXBcIjp7XCJwbGF0Zm9ybV9pZFwiOjMsXCJjb250ZW50X3ByZXNldF9ncm91cF9pZFwiOjAsXCJjcml0ZXJpYVwiOlwiXCIsXCJpZFwiOjEsXCJ0aXRsZVwiOlwiXCJ9LFwiZXh0aWRcIjpcIjEyM1wiLFwic3Vic2NyaWJlclwiOntcImdyb3Vwc1wiOlt7XCJpZFwiOjM0MDYyLFwiZXh0aWRcIjpcImV2ZXJ5b25lXCJ9XSxcImV4dGlkXCI6XCJlcjpndWVzdFwiLFwic3Vic2NyaWJlcl90eXBlXCI6XCJCMkNcIixcImlzX2d1ZXN0XCI6dHJ1ZSxcInR5cGVcIjpcInN1YnNjcmliZXJcIixcImlkXCI6MzQwNTN9LFwicGxhdGZvcm1cIjp7XCJvcGVyYXRvclwiOntcInRpdGxlXCI6XCJcIixcImlkXCI6MixcImV4dGlkXCI6XCJlclwifSxcInRpdGxlXCI6XCJcIixcImlkXCI6MyxcImV4dGlkXCI6XCJvdHR3ZWJcIn0sXCJhdHRyc1wiOm51bGwsXCJncm91cHNcIjpbe1wiaWRcIjoxMzAxODU5NjMsXCJleHRpZFwiOlwiZXI6ZG9tYWluOmd1ZXN0XCJ9LHtcImlkXCI6MzQxOTcsXCJleHRpZFwiOlwiZXI6ZXZlcnlvbmVcIn1dLFwib3BlcmF0b3JcIjp7XCJ0aXRsZVwiOlwiXCIsXCJpZFwiOjIsXCJleHRpZFwiOlwiZXJcIn0sXCJ0eXBlXCI6XCJkZXZpY2VcIixcImlkXCI6MjU4OTk2NTd9fSIsInNpZ25hdHVyZSI6ImNNaE1MWUxRU1wvR1Z5ZWdpNkVHYjQ5WmpFamozU2hjNGRoZFpydGRaR0hzPSJ9'


vanya = {'addr': 'http://testasr.rd.ertelecom.ru/search',
         'headers': {'Content-Type': 'application/json',
                     'accept': 'application/json',
                     'X-Auth-Token': TOKEN
                     },
         'ranker': '',  # experimental, proximity_bm25, bm25, none, wordcount, proximity, matchany, fieldmask, sph04, expr; default: experimental
         'threshold_1': 12,
         'threshold_2': 50
         }


# sergey_bert_1 = {'addr': 'http://93.190.51.59/v3/search',
#                  'headers': {'Content-Type': 'application/json'},
#                  'ranker': '',
#                  'threshold_1': 10,
#                  'threshold_2': 50
#                  }

sergey_bert_1 = {'addr': 'http://77.232.23.74:8008/v1/search',
                 'headers': {'Content-Type': 'application/json'},
                 'ranker': '',
                 'threshold_1': 10,
                 'threshold_2': 50
                 }

sergey_bert_matnicore = {'addr': 'http://77.232.23.74:8008/v3/search',
                         'headers': {'Content-Type': 'application/json'},
                         'ranker': '',
                         'threshold_1': 10,
                         'threshold_2': 50
                         }

movix = {'addr': 'https://discovery-stb3.ertelecom.ru/api/v3/pages/search',
         'headers': {'Content-Type': 'application/json',
                     'X-Auth-Token': TOKEN,
                     'view': 'default'},
         }
