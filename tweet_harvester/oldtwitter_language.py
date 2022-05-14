import json
from textblob import TextBlob
import sys
import argparse
from tweepy import OAuthHandler
import pandas as pd
import numpy as np
import re

def convert_language_name(lang):
    lang_dict = [{'code': 'en', 'name': 'English'}, {'code': 'ar', 'name': 'Arabic'}, {'code': 'bn', 'name': 'Bengali'},
                 {'code': 'cs', 'name': 'Czech'}, {'code': 'da', 'name': 'Danish'}, {'code': 'de', 'name': 'German'},
                 {'code': 'el', 'name': 'Greek'}, {'code': 'es', 'name': 'Spanish'}, {'code': 'fa', 'name': 'Persian'},
                 {'code': 'fi', 'name': 'Finnish'}, {'code': 'fil', 'name': 'Filipino'},
                 {'code': 'fr', 'name': 'French'},
                 {'code': 'he', 'name': 'Hebrew'}, {'code': 'hi', 'name': 'Hindi'}, {'code': 'hu', 'name': 'Hungarian'},
                 {'code': 'id', 'name': 'Indonesian'}, {'code': 'it', 'name': 'Italian'},
                 {'code': 'ja', 'name': 'Japanese'},
                 {'code': 'ko', 'name': 'Korean'}, {'code': 'msa', 'name': 'Malay'}, {'code': 'nl', 'name': 'Dutch'},
                 {'code': 'no', 'name': 'Norwegian'}, {'code': 'pl', 'name': 'Polish'},
                 {'code': 'pt', 'name': 'Portuguese'},
                 {'code': 'ro', 'name': 'Romanian'}, {'code': 'ru', 'name': 'Russian'},
                 {'code': 'sv', 'name': 'Swedish'},
                 {'code': 'th', 'name': 'Thai'}, {'code': 'tr', 'name': 'Turkish'}, {'code': 'uk', 'name': 'Ukrainian'},
                 {'code': 'ur', 'name': 'Urdu'}, {'code': 'vi', 'name': 'Vietnamese'},
                 {'code': 'zh', 'name': 'Chinese'},{'code': 'und', 'name': 'Unknown'},
                {'code': 'in', 'name': 'Indonesian'},{'code': 'tl', 'name': 'Tagalog'},
                {'code': 'et', 'name': 'Estonian'},{'code': 'ht', 'name': 'Haitian Creole'}]

    for language in lang_dict:
        if lang == language['code']:
            lang = language['name']
            return lang
    return lang

df=pd.read_csv('twitter.csv')

#calculate language count by sa4name and year
multilang=df.groupby(['sa4name','language','year'],as_index=False)['user_id'].nunique()

subdict={}
for i in range(0,len(multilang['sa4name'])):
    loc=multilang['sa4name'][i]+str(multilang['year'][i])
    if loc not in subdict.keys():
        subdict[loc]=[(convert_language_name(multilang['language'][i]),int(multilang['user_id'][i]))]
    else:
        subdict[loc].append((convert_language_name(multilang['language'][i]),int(multilang['user_id'][i])))

#calculate sum of language count
totallang=multilang.groupby(['sa4name','year'],as_index=False)['user_id'].sum()
totaldict={}
for i in range(0,len(totallang['sa4name'])):
    loc=totallang['sa4name'][i]+str(totallang['year'][i])
    totaldict[loc]=int(totallang['user_id'][i])

#take top 10 languages
suburb=[]
langcount=[]
for key,value in subdict.items():
    suburb.append(key)
    langcount.append(sorted(value, key = lambda count:count[1], reverse = True)[:10])

#upload
try:
    couchclient = couchdb.Server('http://admin:chocolate_milkshake@172.26.129.34:5984/')

    lang_db_name = 'oldtwitter_language'

    # Check the duplication of database
    try:
        lang_db = couchclient[lang_db_name]
        print(lang_db_name + " has already in the server!")
    except couchdb.http.ResourceNotFound:
        lang_db = couchclient.create(lang_db_name)
        print("Create " + lang_db_name + " in the server!")
    print("Connected to the user database")

except:
    print("Cannot find CouchDB Server ... Exiting\n")
    print("----_Stack Trace_-----\n")
    raise

for i in range(0, len(suburb)):
    doc = {'suburb': suburb[i][:-4], 'year': int(suburb[i][-4:]), 'Language_count': langcount[i],
           'Total_count': totaldict[suburb[i]]}
    print(doc)
    lang_db.save(doc)