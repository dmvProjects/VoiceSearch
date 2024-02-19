TOKEN = 'eyJkYXRhIjoie1wiZXhwaXJlc1wiOjE3MTA5Mjk3MjYsXCJsaWZlc3BhblwiOjI1OTIwMDAsXCJwcmluY2lwYWxcIjp7XCJleHRpZFwiOlwibWFjOkY4OkYwOjgyOjRCOkY0OjY5XCIsXCJzdWJzY3JpYmVyXCI6e1wiZ3JvdXBzXCI6W3tcImlkXCI6MzUwMzcsXCJleHRpZFwiOlwiZXI6ZG9tYWluOnBlcm1cIn1dLFwiZXh0aWRcIjpcInBlcm06NTkwMDIxODUzMTAwXCIsXCJzdWJzY3JpYmVyX3R5cGVcIjpcIkIyQ1wiLFwiaXNfZ3Vlc3RcIjpmYWxzZSxcInR5cGVcIjpcInN1YnNjcmliZXJcIixcImlkXCI6MTI4MjIyNTU4fSxcInBsYXRmb3JtXCI6e1wib3BlcmF0b3JcIjp7XCJ0aXRsZVwiOlwiXCIsXCJpZFwiOjIsXCJleHRpZFwiOlwiZXJcIn0sXCJ0aXRsZVwiOlwiXCIsXCJpZFwiOjExOSxcImV4dGlkXCI6XCJhbmRyb2lkdHZfc3RiXCJ9LFwiZ3JvdXBzXCI6W3tcImlkXCI6MzQxOTcsXCJleHRpZFwiOlwiZXI6ZXZlcnlvbmVcIn1dLFwib3BlcmF0b3JcIjp7XCJ0aXRsZVwiOlwiXCIsXCJpZFwiOjIsXCJleHRpZFwiOlwiZXJcIn0sXCJ0eXBlXCI6XCJkZXZpY2VcIixcImlkXCI6MTMyOTQxMzI5fX0iLCJzaWduYXR1cmUiOiJSeW80WURDc3IzMG1RUlpnb3BpSkc0VVZFdE9QOHhxUy9jYkJUUVd5WnJRPSJ9'

text = 'человек'

# vanya = {'addr': 'http://testasr.rd.ertelecom.ru/search',
#          'headers': {'Content-Type': 'application/json',
#                      'accept': 'application/json',
#                      'X-Auth-Token': TOKEN
#                      },
#          'ranker': '',  # experimental, proximity_bm25, bm25, none, wordcount, proximity, matchany, fieldmask, sph04, expr; default: experimental
#          'threshold_1': 12,
#          'threshold_2': 50
#          }
#
#
# sergey_bert_1 = {'addr': 'http://93.190.51.59/v3/search',
#                  'headers': {'Content-Type': 'application/json'},
#                  'ranker': '',
#                  'threshold_1': 10,
#                  'threshold_2': 50
#                  }
#
# sergey_bert_1 = {'addr': 'http://77.232.23.74:8008/v1/search',
#                  'headers': {'Content-Type': 'application/json'},
#                  'ranker': '',
#                  'threshold_1': 10,
#                  'threshold_2': 50
#                  }
#
# sergey_bert_matnicore = {'addr': 'http://77.232.23.74:8008/search',
#                          'headers': {'Content-Type': 'application/json'},
#                          'ranker': '',
#                          'threshold_1': 10,
#                          'threshold_2': 50
#                          }
#
# sergey_bert_matnicore_prod = {'addr': 'http://testasr.rd.ertelecom.ru:8008/pages/search',
#                               'headers': {'Content-Type': 'application/json'},
#                               'ranker': '',
#                               'threshold_1': 10,
#                               'threshold_2': 50
#                               }


just_ai = {'addr': 'https://zb04.just-ai.com/chatadapter/chatapi/GWkawWVR:9b748aac98bc677b10310a60fd4e225fd0a01099',
           'headers': {'Content-Type': 'application/json'},
           }

movix_showcases = {'addr': 'https://discovery-stb3.ertelecom.ru/api/v3/pages/search',
                   'headers': {'Content-Type': 'application/json',
                               'X-Auth-Token': TOKEN,
                               'view': 'stb3',
                               # 'X-Device-Info': 'mac:DC:DF:D6:B7:D2:11',
                               # 'X-Agreement': '590017751764',
                               'X-App-Version': '2.5.3-2012282712',
                               # 'User-Agent': 'okhttp/3.12.6 com.ertelecom.domrutvstb/2.5.3-2012282712'
                               },
                   }

movix_suggests = {'addr': 'https://discovery-stb3.ertelecom.ru/api/v3/suggests/search',
                  'headers': {'Content-Type': 'application/json',
                              'X-Auth-Token': TOKEN,
                              'view': 'stb3',
                              # 'X-Device-Info': 'mac:DC:DF:D6:B7:D2:11',
                              # 'X-Agreement': '590017751764',
                              'X-App-Version': '2.5.3-2012282712',
                              # 'User-Agent': 'okhttp/3.12.6 com.ertelecom.domrutvstb/2.5.3-2012282712'
                              },
                  }

bert_showcases = {'addr': 'http://158.160.48.107/pages/search',
                  'headers': {'Content-Type': 'application/json',
                              'X-Auth-Token': TOKEN,
                              },
                  }

bert_suggests = {'addr': 'http://158.160.48.107/search',
                 'headers': {'Content-Type': 'application/json',
                             'X-Auth-Token': TOKEN
                             },
                 }
