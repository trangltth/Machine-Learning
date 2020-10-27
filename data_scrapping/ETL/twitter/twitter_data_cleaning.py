import codecs, base64
from ETL.twitter import twitter_data_extraction as te
from urllib.parse import quote_plus
from constants import twitter
import json
from string import Formatter

def cleaning_tweet(raw_tweets):
    raw_tweets_dict = dict(raw_tweets)
    tweets_list = raw_tweets_dict['statuses']

    for tweet in tweets_list:
        print(tweet)

def get_all_users(raw_data_user):
    raw_data_user_dict = dict(raw_data_user)
    user_list = raw_data_user_dict['users']

    for user in user_list:
        print(user)


# get all tweets in Data list
# steps:
# - get all members in Data list
# - lookup members and retrieve tweets

# Tasks:
# add debug function

if __name__ == '__main__':
    get_all_member_param = 'list_id=1291391921135353857'
    user_timeline_params = 'user_id=765548&count=200'
    
    # get all member in Data list
    all_members = te.get_tweet_timeline(twitter.all_members_api, get_all_member_param)
    all_members = json.loads(all_members)
    get_all_users(all_members)

    # get tweets by user
    tweets_by_hilary_mason = te.get_tweet_timeline(twitter.user_timeline_api, user_timeline_params)
    print(tweets_by_hilary_mason)
    tweets_by_hilary_mason = json.loads(tweets_by_hilary_mason)
    for _date in tweets_by_hilary_mason:
        print(_date['created_at'])
        print(_date)





