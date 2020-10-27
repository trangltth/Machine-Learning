import hmac, hashlib, base64
from urllib.parse import quote_plus

#################### Twitter Setting Information ################
# keys & serects
api_key = 'npFLvSrwYooQgcFpJH4XMAaLp'
api_key_serect = 'p28i5zRlyimSr59QWeRiOEvVoUx1Ukl5GNqAIQOvDffJNsaBio'
bearer_token = '''AAAAAAAAAAAAAAAAAAAAAGFdGgEAAAAAn9nnHK%2FMrJ6Qvb0L7SxSS%2BgQCXY%3DIRLsZSRiyAgOk8F1gb2Fi2kSBPwHfIGkmwTcLe01VhFIuU4uZp'''
access_token = '847215515558739968-PYsYMsXr0Kz0wiqncFjad568EDXFd9n'
access_token_serect = 'bF1d2UQEpgvvrWqeHB1qdfQjCc4oSX01v63SBafznxhKM'
signing_key = quote_plus(api_key_serect) + '&' + quote_plus(access_token_serect)

################## Database Connection Setting ##################
db_connection = 'dbname=twitter_clawer user=trang port=5432 password=P@ssw0rd123'

################### Urls & APIs #######################
########## Lists apis ############
all_lists_api = 'https://api.twitter.com/1.1/lists/list.json'

########## url ############
search_url = 'https://twitter.com/search'

########## tweet timeline apis ###################
tweet_home_timeline_api = 'https://api.twitter.com/1.1/statuses/home_timeline.json'
tweet_user_timeline_api = 'https://api.twitter.com/1.1/statuses/user_timeline.json'

########## search apis ###############
search_api = 'https://api.twitter.com/1.1/search/tweets.json'

########## lists apis ###################
all_members_api = 'https://api.twitter.com/1.1/lists/members.json'
list_api = 'https://api.twitter.com/1.1/lists/members/show.json'

########## tweet-fileter realtime apis ###########
tweet_filter_realtime_api = 'https://stream.twitter.com/1.1/statuses/filter.json'

########## geo-apis #######
reverse_geocode_api = 'https://api.twitter.com/1.1/geo/reverse_geocode.json'

######### sample realtime tweet apis #########
statuses_sample = 'https://stream.twitter.com/1.1/statuses/sample.json'

######### user apis ##########
all_followers_api = 'https://api.twitter.com/1.1/followers/list.json'
account_setting_api = 'https://api.twitter.com/1.1/account/settings.json'
account_verify_credential_api = 'https://api.twitter.com/1.1/account/verify_credentials.json'
all_users_api = 'https://api.twitter.com/1.1/users/lookup.json'
friend_list_api = 'https://api.twitter.com/1.1/friends/list.json'



