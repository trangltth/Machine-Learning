import codecs, base64
import twitter_data_extraction as te
from urllib.parse import quote_plus
from constants import twitter
import json
from string import Formatter

####### 2020-08-22 ############
###### Get all users in Data List ######
###### Get all tweets in each members - sample: hilary mason #########
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
    search_params = 'q=' + quote_plus('list:trangletth/Data') + '&result_type=popular'
    get_all_member_param = 'list_id=1291391921135353857'
    tweets_by_user_param = 'follow=807095'
    base_location_param = 'lat=40.6943&long=-73.9249'
    all_follower_param = 'cursor=-1&screen_name='+ quote_plus('trangletth')
    all_users_params = 'screen_name=trangletth'
    user_timeline_params = 'user_id=765548&count=200'

    raw_tweets = te.get_tweet_timeline(twitter.search_api, search_params)
    raw_tweets = json.loads(raw_tweets)

    # get profile
    profile_information = te.get_tweet_timeline(twitter.account_setting_api, '')
    print(profile_information)

    # get account verify credential
    account_credential = te.get_tweet_timeline(twitter.account_verify_credential_api, '')
    print(account_credential)

    # get all users from log in account
    all_users = te.get_tweet_timeline(twitter.all_users_api, all_users_params)
    print(all_users)

    # get all followers
    all_followers = te.get_tweet_timeline(twitter.all_followers_api, all_follower_param)
    print(all_follower_param)
    print(all_followers)

    # get all friends
    all_friends = te.get_tweet_timeline(twitter.friend_list_api, 'cursor=-1&screen_name=trangletth&count=100')

    # print(all_friends)
    all_friends = json.loads(all_friends)
    for friend in all_friends['users']:
        if friend['name'] == 'The New York Times':
            print(friend)

    # get all member in Data list
    all_members = te.get_tweet_timeline(twitter.all_members_api, get_all_member_param)
    all_members = json.loads(all_members)
    get_all_users(all_members)

    # get place
    places_by_base_location = te.get_tweet_timeline(twitter.reverse_geocode_api, base_location_param)
    # print(places_by_base_location)

    # get tweets by user
    tweets_by_hilary_mason = te.get_tweet_timeline(twitter.user_timeline_api, user_timeline_params)
    print(tweets_by_hilary_mason)
    tweets_by_hilary_mason = json.loads(tweets_by_hilary_mason)
    for _date in tweets_by_hilary_mason:
        print(_date['created_at'])

    # get sample realtime tweets 
    # sample_tweets = te.get_tweet_timeline(twitter.statuses_sample, '')
    # print(sample_tweets)



### [Date]
# cleaning types 
# 1. 85 years ago today Social Security was signed into law, but just last week Trump said he\\u2019ll defund Social Security\\u2026 
# 2. https:\\/\\/t.co\\/LCGyfyzVq2
# 3. 19.00 \\u0e19. \\u0e15\\u0e23.\\u0e19\\u0e2d\\u0e01\\u0e40\\u0e04\\u0e23\\u0e37\\u0e48\\u0e2d\\u0e07\\u0e41\\u0e1a\\u0e1a2\\u0e19\\u0e32\\u0e22 \\u0e40\\u0e14\\u0e34\\u0e19\\u0e21\\u0e32\\u0e1a\\u0e2d\\u0e01\\u0e40\\u0e1e\\u0e37\\u0e48\\u0e2d\\u0e19\\u0e40\\u0e1e\\u0e19\\u0e01\\u0e27\\u0e34\\u0e19\\u0e27\\u0e48\\u0e32 \\u0e40\\u0e1e\\u0e19\\u0e01\\u0e27\\u0e34\\u0e19\\u0e2d\\u0e22\\u0e32\\u0e01\\u0e44\\u0e14\\u0e49\\u0e42\\u0e17\\u0e23\\u0e28\\u0e31\\u0e1e\\u0e17\\u0e4c \\u0e42\\u0e14\\u0e22\\u0e08\\u0e30\\u0e1e\\u0e32\\u0e40\\u0e1e\\u0e37\\u0e48\\u0e2d\\u0e19\\u0e17\\u0e31\\u0e49\\u0e07\\u0e2a\\u0e2d\\u0e07\\u0e40\\u0e02\\u0e49\\u0e32\\u0e44\\u0e1b\\u0e17\\u0e32\\u0e07\\u0e14\\u0e49\\u0e32\\u0e19\\u0e2b\\u0e25\\u0e31\\u2026 https:\\/\\/t.co\\/WuAYTP8JV5
# https://t.co/WuAYTP8JV5


# text = '85 years ago today Social Security was signed into law, but just last week Trump said he\u2019ll defund Social Security\u2026'
# content = '\u0e19. \u0e15\u0e23.\u0e19\u0e2d\u0e01\u0e40\u0e04\u0e23\u0e37\u0e48\u0e2d\u0e07\u0e41\u0e1a\u0e1a2\u0e19'

# text_decoding = text.encode('utf-8_sig').decode('utf-8_sig')
# content_decoding = content.encode('utf-8_sig').decode('utf-8_sig')

# print(text_decoding)
# print(content_decoding)


