import logging
import time
import sys

import couchdb
from textblob import TextBlob

import tweepy
from tweepy import Stream

RETRY_COUNT = 3
DB_NAME = 'new_tweets'

class MyStreamListener(Stream):
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, tweet_db, **kwargs):
        super().__init__(consumer_key, consumer_secret, access_token, access_token_secret, **kwargs)
        self.tweet_db = tweet_db
        self.count = 0
    
    def on_status(self, status):
        retweeted = status.retweeted
        if retweeted == False:
            # Get required information
            text = status.text
            username = status.user.screen_name
            id_str = status.id_str
            createtime = str(status.created_at)
            userlocation = status.user.location
            lang = status.lang
            geo = status.geo
        
            # Conduct analysis on tweet
            blob = TextBlob(text)
            sent = blob.sentiment
            polarity = sent.polarity
            subjectivity = sent.subjectivity

            # Save tweet to DB
            self.tweet_db.save({"id": id_str, "createtime": createtime, "text": text, "username": username,
                           "userlocation": userlocation, "lang": lang, "geo": geo,
                           "polarity": polarity, "subjectivity": subjectivity})
            self.count += 1
            #print(f"{self.count:>5d}: {text}")
            logging.info(f"{self.count:>5d}: Status {id_str} collected")
        else:
            #print(f"{-1:>5} Retweet ignored")
            pass

    def on_error(self, status_code):
        if status_code == 420:  # end of monthly limit rate (500k)
            time.sleep(10)
            return False


def get_api(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

def get_couchdb_client(user, pwd, host, port=5984):
    client = couchdb.Server(f"http://{user}:{pwd}@{host}:{port}/")
    logging.info(f"Connected to CoudhDB at http://{user}:{pwd}@{host}:{port}/")
    return client

def get_tweet_database(client, dbname='melb_tweets'):
    if dbname in client:
        logging.info(dbname + "already exists in CouchDB")
    else:
        client.create(dbname)
        logging.info(dbname + "created in CouchDB")
    return client[dbname]

################################################################################

if __name__ == '__main__':
    current_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    logging.basicConfig(#filename='tweet_harvester-{}.log'.format(current_time),
                        #filemode='a',
                        format='[%(asctime)s] %(name)s %(levelname)s %(message)s',
                        datefmt="%Y/%m/%d %H:%M:%S",
                        level=logging.INFO)
    
    if len(sys.argv) != 8:
        logging.critical("Incorrect format for initialising the harvester")
        logging.info("Format: python3 stream.py <consumer key> <consumer secret> <access token> <access token secret> <couch db usr> <couch db pwd> <coudh db address>")
        sys.exit(1)
    
    consumer_key, consumer_secret, access_token, access_token_secret = sys.argv[1:5]
    db_user, db_pwd, db_address = sys.argv[5:8]
    try:
        logging.info("Initialising harvester...")
        twt_api = get_api(consumer_key, consumer_secret, access_token, access_token_secret)
        db_client = get_couchdb_client(db_user, db_pwd, db_address)
        tweet_db = get_tweet_database(db_client, DB_NAME)
    except:
        logging.critical("An critical error occured when initialisng harvester, exiting...")
        sys.exit(1)

    retry_count = RETRY_COUNT
    

    logging.info("Initialisation complete! Now start streaming...")
    while (retry_count):
        try:
            logging.info(f"Stream starts. {retry_count} retry/retries remaining.")
            stream = MyStreamListener(consumer_key, consumer_secret, access_token, access_token_secret, tweet_db)
            stream.filter(track=["melb", 'Melb', 'MELB', 'melbourne', 'Melbourne', 'MELBOURNE'])
        except:
            logging.exception("An error during streaming")
            time.sleep(10)
            retry_count -= 1
    
    logging.info("No more retries available, exiting...")
    sys.exit(0)
