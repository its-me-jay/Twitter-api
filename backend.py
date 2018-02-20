import oauth2 as oauth
import json
from bs4 import BeautifulSoup
import urllib
from datetime import datetime
from email.utils import parsedate_tz, mktime_tz
import pytz
from pymongo import MongoClient

client=MongoClient()
db=client.twitter
collection=db.api1


CONSUMER_KEY = "Put_your_application's_consumerkey"
CONSUMER_SECRET = "Put_your_application's_consumerSecret"
ACCESS_KEY = "Put_your_application's_Accesskey"
ACCESS_SECRET = "Put_your_application's_AccessSecret"
consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
client = oauth.Client(consumer, access_token)
response, data = client.request("https://api.twitter.com/1.1/help/languages.json")
languages=json.loads(data

def build_url(keyword):
    main_url="https://api.twitter.com/1.1/search/tweets.json?"
    url_tail={'q':keyword,'count':100}
    url_tail=urllib.urlencode(url_tail)
    url=main_url+url_tail
    return url

def language(language_code):
    i=0
    for i in range(len(languages)):
        if(language_code==languages[i]['code']):
            return languages[i]['name']
                     
def twitter_search(keyword):
    url=build_url(keyword)
    response, data = client.request(url)
    data=json.loads(data)
    for i in range(len(data['statuses'])):

        if "retweeted_status" in list(data['statuses'][i]):
            retweets=data['statuses'][i]['retweeted_status']['retweet_count']
            favorites=data['statuses'][i]['retweeted_status']['favorite_count']
            hashtags=[(data['statuses'][i]['retweeted_status']['entities']['hashtags'][j]['text']).encode('utf-8') for j in range(len(data['statuses'][i]['retweeted_status']['entities']['hashtags']))]
            tweet_text=(data['statuses'][i]['retweeted_status']['text']).encode('utf-8')
            tweet_language=language(data['statuses'][i]['retweeted_status']['metadata']['iso_language_code'])

            timestamp = mktime_tz(parsedate_tz(data['statuses'][i]['retweeted_status']['created_at']))
            tweet_time = datetime.fromtimestamp(timestamp, pytz.timezone('Asia/Kolkata')).isoformat()
            tweet_time=str(tweet_time[0:-6]+"Z")
            tweet_time = datetime.strptime(tweet_time, "%Y-%m-%dT%H:%M:%SZ")
            #tweet_time=tweet_time.strftime('%Y-%m-%d %H:%M:%S')
            tweet_id=data['statuses'][i]['retweeted_status']['id']
            tweet_link="https://twitter.com/statuses/"+str(tweet_id)

            user_followersCount=data['statuses'][i]['retweeted_status']['user']['followers_count']
            user_favouritesCount=data['statuses'][i]['retweeted_status']['user']['favourites_count']
            user_friends=data['statuses'][i]['retweeted_status']['user']['friends_count']
            user_name=(data['statuses'][i]['retweeted_status']['user']['name']).encode('utf-8')
            user_screenname=(data['statuses'][i]['retweeted_status']['user']['screen_name']).encode('utf-8')
            user_profileLink="https://twitter.com/"+str(user_screenname)
            user_language=language(data['statuses'][i]['retweeted_status']['user']['lang'])
            try :
                db_document={"_id":tweet_id,"retweets":retweets,"favorites":favorites,"hashtags":hashtags,"tweet_text":tweet_text,"tweet_language":tweet_language,"tweet_time":tweet_time,"tweet_link":tweet_link,"user_name":user_name,"user_screenname":user_screenname,"user_profileLink":user_profileLink,"user_language":user_language,"user_friends":user_friends,"user_followersCount":user_followersCount,"user_favouritesCount":user_favouritesCount}
                collection.insert_one(db_document)
            except:
                pass

        else:
            retweets=data['statuses'][i]['retweet_count']
            favorites=data['statuses'][i]['favorite_count']
            hashtags=[(data['statuses'][i]['entities']['hashtags'][j]['text']).encode('utf-8') for j in range(len(data['statuses'][i]['entities']['hashtags']))]
            tweet_text=(data['statuses'][i]['text']).encode('utf-8')
            tweet_language=language(data['statuses'][i]['metadata']['iso_language_code'])

            timestamp = mktime_tz(parsedate_tz(data['statuses'][i]['created_at']))
            tweet_time = datetime.fromtimestamp(timestamp, pytz.timezone('Asia/Kolkata')).isoformat()
            tweet_time=str(tweet_time[0:-6]+"Z")
            tweet_time = datetime.strptime(tweet_time, "%Y-%m-%dT%H:%M:%SZ")
            #tweet_time=tweet_time.strftime('%Y-%m-%d %H:%M:%S')
            tweet_id=data['statuses'][i]['id']
            tweet_link="https://twitter.com/statuses/"+str(tweet_id)

            user_followersCount=data['statuses'][i]['user']['followers_count']
            user_favouritesCount=data['statuses'][i]['user']['favourites_count']
            user_friends=data['statuses'][i]['user']['friends_count']
            user_name=(data['statuses'][i]['user']['name']).encode('utf-8')
            user_screenname=(data['statuses'][i]['user']['screen_name']).encode('utf-8')
            user_profileLink="https://twitter.com/"+str(user_screenname)
            user_language=language(data['statuses'][i]['user']['lang'])
            try:
                db_document={"_id":tweet_id,"retweets":retweets,"favorites":favorites,"hashtags":hashtags,"tweet_text":tweet_text,"tweet_language":tweet_language,"tweet_time":tweet_time,"tweet_link":tweet_link,"user_name":user_name,"user_screenname":user_screenname,"user_profileLink":user_profileLink,"user_language":user_language,"user_friends":user_friends,"user_followersCount":user_followersCount,"user_favouritesCount":user_favouritesCount}
                collection.insert_one(db_document)
            except:
                pass
