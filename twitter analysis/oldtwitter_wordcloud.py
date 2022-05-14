import json
from textblob import TextBlob
import sys
import argparse
from tweepy import OAuthHandler
import pandas as pd
import numpy as np
import re
from collections import Counter


df=pd.read_csv('twitter.csv')

#employment
kwdls=['employ','job','occupation','career','profession','out of work','resign','leave office','dimission','lay off','unpaid leave','salary','income','wage','compensation']
row=[]
for i in range(0,len(df['tweet'])):
    for word in kwdls:
        if word in df['tweet'][i]:
            row.append(i)
            break
employment=df.loc[row]
employmentls=countword(employment)

#housing
kwdls=['house','housing','rent','tenement','vacancies','vacancy','apartment','vacant','resident','lodgings','room','accommodation','tenant','salary','income','wage','compensation']
row=[]
for i in range(0,len(df['tweet'])):
    for word in kwdls:
        if word in df['tweet'][i]:
            row.append(i)
            break
housing=df.loc[row]
rentls=countword(housing)

#environment
kwdls=['environment','infrastructure','tour','visit','travel','pollution','scenary','landscape','surroundings','air','weather','nature','architecture','rain','humidity','temperature','barometer','hpa','drowning']
row=[]
for i in range(0,len(df['tweet'])):
    for word in kwdls:
        if word in df['tweet'][i]:
            row.append(i)
            break
environment=df.loc[row]
environmentls=countword(environment)

#livability
kwdls=['ill','life','expectancy','live','sick','happy','happiness','love','good','boring','wonderful','sad']
row=[]
for i in range(0,len(df['tweet'])):
    for word in kwdls:
        if word in df['tweet'][i]:
            row.append(i)
            break
life=df.loc[row]
lifels=countword(life)


try:
    couchclient = couchdb.Server('http://admin:chocolate_milkshake@172.26.129.34:5984/')

    lang_db_name = 'oldtwitter_wordcloud'

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

word = ['employment', 'housing', 'environment', 'livability']
ls = [employmentls, rentls, environmentls, lifels]
for i in range(0, len(ls)):
    doc = {word[i]: ls[i]}
    print(doc)
    lang_db.save(doc)

# df=pd.DataFrame({'employment':employmentls,'rent':rentls,'environment':environmentls,'happiness':lifels})
# df.to_excel('cloud.xlsx')