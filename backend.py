import oauth2 as oauth
import json
from bs4 import BeautifulSoup
import urllib


CONSUMER_KEY = "Put_your_application's_consumerkey"
CONSUMER_SECRET = "Put_your_application's_consumerSecret"
ACCESS_KEY = "Put_your_application's_Accesskey"
ACCESS_SECRET = "Put_your_application's_AccessSecret"

def build_url(keyword):
    main_url="https://api.twitter.com/1.1/search/tweets.json?"
    url_tail={'q':keyword,'count':100}
    url_tail=urllib.urlencode(url_tail)
    url=main_url+url_tail
    return url


consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
client = oauth.Client(consumer, access_token)

timeline_endpoint = "https://api.twitter.com/1.1/search/tweets.json?q=%23PadManChallenge"
response, data = client.request(timeline_endpoint)



tweets = json.loads(data)
print tweets
print("----------------------------------------------------------------")
soup=BeautifulSoup(data,'html.parser')
print soup.prettify()
