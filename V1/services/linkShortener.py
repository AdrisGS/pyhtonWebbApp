# import requests

# headers = {
#     'Authorization': 'Bearer {0ee4122fadbf5fdaa1f7dade81773cb2253ff1e7}',
#     'Content-Type': 'application/json',
# }

# data = '{ "long_url": "https://realpython.com/python-requests/", "domain": "bit.ly", "group_guid": "o_4go7qpvagm" }'

# response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, data=data)
# print(response.content)
# print(response.text)

import urllib.request
# import sys

def tiny_url(url):
    apiurl = "http://tinyurl.com/api-create.php?url="
    tinyurl = urllib.request.urlopen(apiurl + url).read()
    return tinyurl.decode("utf-8")
# print(tiny_url('https://pypi.org/project/short_url/'))
# url = sys.argv[1]
# print(url)
# print(tiny_url(url))


# import requests
# api='https://cutt.ly/api/api.php'
# key = '92d985e29b4ef846f063203269419aaf9f60c'
# long_url = 
# randome_short = 
# response = response.post('')
# https://cutt.ly/api/api.php?key=92d985e29b4ef846f063203269419aaf9f60c&short=https://github.com/FaztWeb/flask-crud-contacts-app/tree/master/templates&name=cccPayLink
# 92d985e29b4ef846f063203269419aaf9f60c

