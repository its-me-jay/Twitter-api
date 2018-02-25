from pymongo import MongoClient
from datetime import datetime

client=MongoClient()
db=client.twitter

def print_document(document):
    keys=["retweets","favorites","hashtags","tweet_text","tweet_language","tweet_time","tweet_link","user_name","user_screenname","user_profileLink","user_language","user_friends","user_followersCount","user_favouritesCount"]
    for x in keys:
        print x + ":-"
        print document[x]
        print " "
    print "---------##### Next Tweet #####---------"
    print " "

def db_search(keyword):
    collection=db.api1
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

def db_search_simplified(keyword):
    collection=db.api1
    keyword=keyword.decode('utf-8')
    cursor=collection.find({"$text":{"$search":keyword}})
    flag=0
    for document in cursor:
        print_document(document)
        flag=1
    if(flag==0):
        print "No matching results found"

def menu():
    print "Choose filters from below"
    print "1: User"
    print "2: Dates"
    print "3: Retweets"
    print "4: Favorites"
    a=raw_input("Enter your choice: \n")
    return a

def db_filters(filters):
    a=int(menu())
    if(a==1):
        arr=[]
        arr.append(a)
        user=raw_input("Enter user name/screen name\n")
        arr.append(user)
        filters.append(arr)
    if(a==2):
        arr=[]
        arr.append(a)
        from_date=raw_input("Enter from date in yyyy-mm-dd hh:mm:ss format\n")
        to_date=raw_input("Enter to date in yyyy-mm-dd hh:mm:ss format\n")
        from_date=from_date.strip().split()
        from_date=str(from_date[0]+"T"+from_date[1]+"Z")
        to_date=to_date.strip().split()
        to_date=str(to_date[0]+"T"+to_date[1]+"Z")

        arr.append(from_date)
        arr.append(to_date)
        filters.append(arr)
    if(a==3):
        arr=[]
        arr.append(a)
        retweets=int(raw_input("Enter number of retweets\n"))
        selection=int(raw_input("Enter 1 for greater than, 2 for less than and 3 for equal to\n"))
        arr.append(retweets)
        arr.append(selection)
        filters.append(arr)
    if(a==4):
        arr=[]
        arr.append(a)
        favorites=int(raw_input("Enter number of favorites\n"))
        selection=int(raw_input("Enter 1 for greater than, 2 for less than and 3 for equal to\n"))
        arr.append(favorites)
        arr.append(selection)
        filters.append(arr)
    a=int(raw_input("Enter 5 to display results and 6 to enter more filters and 7 to display results in sorted manner\n"))
    if(a==5):
        cursor=db_applyFilters(filters)
        db_displayresults(cursor)
    elif(a==6):
        db_filters(filters)
    elif(a==7):
        cursor=db_applyFilters(filters)
        db_sort(cursor)
    else:
        print("Invalid input received -- Exiting....\n")
        return
def db_sort(cursor):
    a=[int(k) for k in raw_input("1: datetime, 2: tweet text, 3: retweets, 4: favorites\n").strip().split()]
    applied_filters=[]
    #collection=db.api1
    for i in range(len(a)):
        if(abs(a[i])==1):
            condition=("tweet_time",abs(a[i])/a[i])
            applied_filters.append(condition)
        if(abs(a[i])==2):
            condition=("tweet_text",abs(a[i])/a[i])
            applied_filters.append(condition)
        if(abs(a[i])==3):
            condition=("retweets",abs(a[i])/a[i])
            applied_filters.append(condition)
        if(abs(a[i])==4):
            condition=("favorites",abs(a[i])/a[i])
            applied_filters.append(condition)
    cursor=cursor.sort(applied_filters)
    flag=0
    for document in cursor:
        print_document(document)
        flag=1
    if(flag==0):
        print "No matching results found"

def db_applyFilters(filters):
    collection=db.api1
    applied_filters={}
    for i in range(len(filters)):
        if(filters[i][0]==1): #username/screenname filter
            user=filters[i][1]
            applied_filters["$or"]=[{"user_name":user},{"user_screenname":user}]

        if(filters[i][0]==2): #datetime filter
            from_date=filters[i][1]
            from_date = datetime.strptime(from_date, "%Y-%m-%dT%H:%M:%SZ")
            to_date=filters[i][2]
            to_date = datetime.strptime(to_date, "%Y-%m-%dT%H:%M:%SZ")
            applied_filters["tweet_time"]={"$gte": from_date,"$lt":to_date}

        if(filters[i][0]==3): #retweets filter
            if(filters[i][2]==1):       #greater than
                retweets=filters[i][1]
                applied_filters["retweets"]={"$gt":retweets}
            if(filters[i][2]==2):       #less than
                retweets=filters[i][1]
                applied_filters["retweets"]={"$lt":retweets}
            if(filters[i][2]==3):       #equal to
                retweets=filters[i][1]
                applied_filters["retweets"]=retweets

        if(filters[i][0]==4): #favorites filter
            if(filters[i][2]==1):       #greater than
                favorites=filters[i][1]
                applied_filters["favorites"]={"$gt":favorites}
            if(filters[i][2]==2):       #less than
                favorites=filters[i][1]
                applied_filters["favorites"]={"$lt":favorites}
            if(filters[i][2]==3):       #equal to
                favorites=filters[i][1]
                applied_filters["favorites"]=favorites
    #print applied_filters
    cursor=collection.find(applied_filters)
    return cursor

def db_displayresults(cursor):
    flag=0
    for document in cursor:
        print_document(document)
        flag=1
    if(flag==0):
        print "No matching results found"

while(1):
    a=int(raw_input("Enter 1 to directly search in db, 2 to put filters and 3 to print the database in sorted manner\n"))
    if(a==2):
        filters=[]
        db_filters(filters)
    elif(a==1):
        keyword=raw_input("Enter keyword\n")
        #db_search_simplified(keyword)
        db_search(keyword)
    elif(a==3):
        collection=db.api1
        db_sort(collection)
    else:
        print "Invalid input received -- Exiting....\n"
