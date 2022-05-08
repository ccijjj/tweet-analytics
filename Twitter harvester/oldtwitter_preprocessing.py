import json
from textblob import TextBlob
import sys
import argparse
from tweepy import OAuthHandler
import pandas as pd
import numpy as np
import re

i=0
with open('D:/twitter/twitter-melb.json', 'r', encoding='utf-8') as f:
    for line in f:
        i+=1

#change coordinate to district
sa4code = {}
sa4name = {}
sa4code2 = {}
sa4name2 = {}
sa4code3 = {}
sa4name3 = {}
sa4codeam = {}
sa4nameam = {}

district = pd.read_csv('australian_postcodes.csv')
for i in range(0, len(district)):
    code = district['SA4_CODE_2016'][i]
    name = district['SA4_NAME_2016'][i]
    coord = str('%.2f' % district['lat'][i]) + ',' + str('%.2f' % district['long'][i])

    if coord not in sa4code.keys():  # 只记录第一个位置
        sa4code[coord] = code
        sa4name[coord] = name

    if coord not in sa4code2.keys():  # 只记录第一个位置
        sa4code2[coord[:-1]] = code
        sa4name2[coord[:-1]] = name
    coord3 = str('%.1f' % district['lat'][i]) + ',' + str('%.2f' % district['long'][i])
    if coord3 not in sa4code3.keys():  # 只记录第一个位置
        sa4code3[coord3] = code
        sa4name3[coord3] = name
    coordam = str('%.1f' % district['lat'][i]) + ',' + str('%.1f' % district['long'][i])
    if coordam not in sa4codeam.keys():  # 只记录第一个位置
        sa4codeam[coordam] = code
        sa4nameam[coordam] = name


# read data
current_line = 1
line_start = 1
line_end = i
idls = []
timels = []
languagels = []
tweetls = []
scorels = []
postcodels = []
locationls = []
coordls = []
user_idls = []
followers_countls = []
sa4codels = []
sa4namels = []
yearls = []
with open('D:/twitter/twitter-melb.json', encoding='utf-8') as f:  # 打开要读的文件
    for line in f:
        postcode = ''
        location = ''
        if current_line == line_end:
            current_line += 1
            break
        if current_line >= line_start:
            if line.startswith('{'):
                if line.endswith('},\n'):
                    content = line[:-2]
                elif line.endswith('}\n'):
                    content = line[:-1]
                else:
                    content = None
            if content and content.count('{') == content.count('}'):
                json_tweet = json.loads(content)
                if json_tweet['id']:
                    # Initially extract some useful information
                    id = json_tweet['id']  # The unique ID of each tweet
                if json_tweet['doc']['text']:
                    text = json_tweet['doc']["text"]  # The text of each tweet
                testimonial = TextBlob(text)
                score = testimonial.sentiment.polarity  # Analysis the sentiment score

                if json_tweet['doc']['created_at']:
                    time = json_tweet['doc']["created_at"]  # The timestamp of post
                if json_tweet['doc']['lang']:
                    language = json_tweet['doc']["lang"]  # The timestamp of post

                if json_tweet['doc']['user']['screen_name']:
                    user_id = json_tweet['doc']['user']["screen_name"]  # The timestamp of post
                if json_tweet['doc']['user']['followers_count']:
                    followers_count = json_tweet['doc']['user']["followers_count"]  # The timestamp of post
                if json_tweet['doc']['geo']:
                    if json_tweet['doc']['geo']['coordinates']:
                        coord = json_tweet['doc']["geo"]['coordinates']  # The geo location information of this tweet
                        coordstr = '%.02f' % coord[0] + ',' + '%.02f' % coord[1]
                        coordstr2 = coordstr[:-1]
                        coordstr3 = '%.01f' % coord[0] + ',' + '%.02f' % coord[1]
                        coordstram = '%.01f' % coord[0] + ',' + '%.01f' % coord[1]
                        if coordstr in postcodedict.keys():
                            postcode = postcodedict[coordstr]
                            location = locationdict[coordstr]
                        elif coordstr2 in postcodedict2.keys():
                            postcode = postcodedict2[coordstr2]
                            location = locationdict2[coordstr2]
                        elif coordstr3 in postcodedict3.keys():
                            postcode = postcodedict3[coordstr3]
                            location = locationdict3[coordstr3]
                        elif coordstram in postcodedictam.keys():
                            postcode = postcodedictam[coordstram]
                            location = locationdictam[coordstram]
                        if coordstr in sa4code.keys():
                            code = sa4code[coordstr]
                            name = sa4name[coordstr]
                        elif coordstr2 in sa4code2.keys():
                            code = sa4code2[coordstr2]
                            name = sa4name2[coordstr2]
                        elif coordstr3 in sa4code3.keys():
                            code = sa4code3[coordstr3]
                            name = sa4name3[coordstr3]
                        elif coordstram in sa4codeam.keys():
                            code = sa4codeam[coordstram]
                            name = sa4nameam[coordstram]

                idls.append(id)
                timels.append(time)
                yearls.append(int(time[-4:]))
                languagels.append(language)
                tweetls.append(text)
                scorels.append(score)
                postcodels.append(postcode)
                locationls.append(location)
                sa4codels.append(code)
                sa4namels.append(name)
                coordls.append(coord)
                user_idls.append(user_id)
                followers_countls.append(followers_count)

df=pd.DataFrame({'_id': idls, "time": timels, "year":yearls,"language": languagels, 'tweet': tweetls, "sensitivityscore": scorels, "postcode": postcodels,"sa4code":sa4codels,"sa4name":sa4namels,"location":locationls, 'geo':coordls,'user_id':user_idls,'followers_count':followers_countls})
df.to_excel('twitter.xlsx')