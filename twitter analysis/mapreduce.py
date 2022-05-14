import json
import couchdb
import requests

view_name = 'myDesignDoc'
db_name = 'new_tweets'
ip = 'http://admin:chocolate_milkshake@172.26.129.34:5984/'
sever = couchdb.Server(ip)
db = sever[db_name]
purpose = 'polarity'

result = json.loads(requests.get(ip + db_name + "/_design/" + view_name + "/_view/" + purpose).text)
# print(result)

sum = result['rows'][0]['value']['sum']
count = result['rows'][0]['value']['count']

average = sum / count
print(average)

purpose2 = 'lang-view'
result2 = json.loads(requests.get(ip + db_name + "/_design/" + view_name + "/_view/" + purpose2).text)['rows']
language_count = {}
for i in range(len(result2)):
    key = result2[i]['key']
    if key not in language_count.keys():
        language_count[key] = 1
    else:
        language_count[key] = language_count[key] + 1

print(language_count)

purpose3 = 'year-count'
result3 = json.loads(requests.get(ip + db_name + "/_design/" + view_name + "/_view/" + purpose3).text)['rows'][0][
    'value']
print(result3)

purpose4 = 'text-view'
result4 = json.loads(requests.get(ip + db_name + "/_design/" + view_name + "/_view/" + purpose4).text)['rows']
time_text = {}
for i in range(len(result4)):
    key = result4[i]['key']
    if key not in time_text.keys():
        time_text[key] = str(result4[i]['value'])
    else:
        time_text[key] = time_text[key] + str((result4[i]['value']))