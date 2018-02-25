# Twitter-api

This api uses standard Twitter search api to fetch tweets corresponding to the keyword user enters.

Proper readme would be uploaded very soon.

# backend.py (API 1)
1) Start Mongodb server on your local machine and create a collection and name it "api1" 
2) Run the code. You will be prompted to enter a keyword to search for. Once the execution is finished, the results are stored automatically into the database.

# db_search.py (API 2)
1) This api is used to perform any operations on the database.
2) Run the code. You will be prompted with three options:

   # 1: To directly search in db:
        This option will let you search for a keyword in database. (Search is performed on fields username,screenname,tweettext and hashtags). It checks, if "entered string is present" in any of the above fields and displays the results.
   # 2: To put filters 
        This option lets you put four types of filters on data.
          1) username/screenname : This option lets you filter all the tweets by a particular user.
          2) Datetime : This option lets you filter all tweets that are created between "from" datetime and "to" datetime.
          3) Retweets: This option lets you filter data based on number of retweets. After choosing this option, you will be prompted to enter "number of retweets"(say X), after that you will be asked to choose greater than or less than or equal to. Suppose if you have choosen greater than, it means that, you have put a filter "all tweets with retweets GREATER THAN X".
          4) Favorites: Same as retweets
          
        (You can put more than one filters by selecting enter more filters)
        
        Once you think you've put enough filters, you can choose to display the results as it is or you can display the results in a sorted manner(we'll discuss about it below)
   # 3: To print the database in sorted manner
       1) This option let's you print the results in a sorted manner.
       2) You will be prompted to enter an input according to "1: datetime, 2: tweet text, 3: retweets, 4: favorites"
          # Understanding how to give input
          Look at the following examples to understand how to give input.
            1) Input :- "4", Meaning: Sort the tweets in ascending order of no. of favorites
            2) Input :- "-4", Meaning: Sort the tweets in descending order of no. of favorites
            3) Input :- "1 2", Meaning: First sort the tweets in ascending order of datetime and sort the RESULTING list in ascending order of tweet text.
            4) Input :- "-1 3 -4", Meaning: Sort the tweets in descending order of datetime and sort the resulting list in ascending order of retweets and then sort the resulting list again in descending order of no. of favorites.
 
 
 If you have any doubts, feel free to raise an issue.
 
 Thanks!
