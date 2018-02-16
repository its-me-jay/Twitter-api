from pymongo import MongoClient

client=MongoClient()
db=client.twitter
collection=db.api1

def print_document(document):
    keys=["retweets","favorites","hashtags","tweet_text","tweet_language","tweet_time","tweet_link","user_name","user_screenname","user_profileLink","user_language","user_friends","user_followersCount","user_favouritesCount"]
    for x in keys:
        print x + ":-"
        print document[x]
        print " "
    print "---------##### Next Tweet #####---------"
    print " "

def db_search(keyword):
    cursor=collection.find({})
    keyword=keyword.decode('utf-8')
    flag=0
    for document in cursor:
        username=document['user_name']
        screenname=document['user_screenname']
        text=document['tweet_text']
        hashtags=document['hashtags']

        if username.find(keyword)!=-1:
            flag=1
            print_document(document)
        if screenname.find(keyword)!=-1:
            flag=1
            print_document(document)
        if text.find(keyword)!=-1:
            flag=1
            print_document(document)
        for tag in hashtags:
            if tag.find(keyword)!=-1:
                flag=1
                print_document(document)
    if(flag==0):
        print "No matching results found"

