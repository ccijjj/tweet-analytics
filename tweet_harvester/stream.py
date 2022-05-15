import tweepy

import couchdb
import configparser
from textblob import TextBlob

from urllib3.exceptions import ProtocolError

import time
import datetime

consumer_key = "qWrrtRVJwGcdlMxomVnHWxHNk"
consumer_secret = "aT9gwPNp7azSwiv9EyXTJhiM4772D6lxx4LqhT8UgrDf3yR0L3"

access_token = "1519554286765867008-gNV0HI3s4PJTqPqYnhIKAEKTecqaHE"
access_token_secret = "V3XKlilsVjktnDydlqi7GkWhBsTKf9lRLf2WxNcMWf6z2"

# consumer_key = 'AOWMzMqc6wUg92K3avHXq8u8s'
# consumer_secret = 'dhHpQSmtb5rODqustlFr4fnq9kGayLUWQvFMPPeCAE5BiUVgZ6'
# access_token = '1519236823960018944-sBQsPxqeRCb1GwbRvtk53RDLmSfiOY'
# access_token_secret = 'R1POlI1Owl5FP1MrdBDcCpkZYpINOm6BMnrL2v8HJLzQf'

# authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

count = 0

try:
    couchclient = couchdb.Server('http://admin:chocolate_milkshake@172.26.129.34:5984/')

    tweet_db_name = 'ccc'

    # Check the duplication of database
    if tweet_db_name in couchclient:
        print(tweet_db_name + " has already in the server!")
        tweet_db = couchclient[tweet_db_name]
    else:
        print("Create " + tweet_db_name + " in the server!")
        tweet_db = couchclient.create(tweet_db_name)
    print("Connected to the user database")
except:
    print("Cannot find CouchDB Server ... Exiting\n")
    print("----_Stack Trace_-----\n")
    raise

from tweepy import Stream


class MyStreamListener(Stream):
    def on_status(self, status):
        global count
        text = status.text

        username = status.user.screen_name
        id_str = status.id_str
        createtime = str(status.created_at)
        userlocation = status.user.location
        lang = status.lang
        retweeted = status.retweeted
        geo = status.geo
        blob = TextBlob(text)
        sent = blob.sentiment
        polarity = sent.polarity
        subjectivity = sent.subjectivity

        if retweeted == False and id_str not in tweet_db:
            tweet_db.save({"id": id_str, "createtime": createtime, "text": text, "username": username,
                           "userlocation": userlocation, "lang": lang, "geo": geo,
                           "polarity": polarity, "subjectivity": subjectivity})
            count += 1
            print(count)
        else:
            pass
        print(status.text)  # prints every tweet received

    def on_error(self, status_code):
        if status_code == 420:  # end of monthly limit rate (500k)
            return False


stream = MyStreamListener(consumer_key,
                          consumer_secret,
                          access_token,
                          access_token_secret)

stream.filter(track=["melb", 'Melb', 'MELB', 'melbourne', 'Melbourne', 'MELBOURNE'])
