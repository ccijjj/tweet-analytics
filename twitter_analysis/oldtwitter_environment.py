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

kwdls=['environment','infrastructure','tour','visit','travel','pollution','scenary','landscape','surroundings','air','weather','nature','architecture','rain','humidity','temperature','barometer','hpa','drowning']
row=[]
for i in range(0,len(df['tweet'])):
    for word in kwdls:
        if word in df['tweet'][i]:
            row.append(i)
            break
environment=df.loc[row]

sensitivity=environment[['sa4name','year','sensitivityscore']]
sensitivity=sensitivity.groupby(['year'],as_index=False)['sensitivityscore'].mean()
sensitivity.to_excel('sensitivity.xlsx')

#total tweets count
count=df[['year','sa4name']]
totalcount=count.groupby(['year'],as_index=False).count()


#environment related tweets count
count=environment[['year','sensitivityscore']]
environmentcount=count.groupby(['year'],as_index=False).count()

compare=totalcount.join(environmentcount.set_index('year'),on='year')
sensitivity.to_excel('sensitivity.xlsx')
compare.to_excel('count.xlsx')


