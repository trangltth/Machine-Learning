import sys
sys.path.append('/home/trang/working/projects/Machine-Learning/data_scrapping')
from ETL.twitter import twitter_data_cleaning as tdc, twitter_data_extraction as tde
from constants import twitter
from packages.object_scrapping.twitter import user, tweet, login_user, o_list, member
import json, psycopg2
from datetime import datetime
from typing import List, Dict, Tuple, TypeVar

psycopg_conn = TypeVar('psycogp_conn')

def getDatatopic(conn, data_list_params):
    # extract_all_member_by_list
    members = tde.extract_data_from_api(twitter.all_members_api, data_list_params)
    members = json.loads(members)
    for member in members['users']:
        _user = user.user(member['id'], member['name'], member['screen_name'], member['location'], member['description'], member['url'], member, member['created_at'], False, member['following'])
        _user.storeDatabase(conn)
    return members['users']

def getTweetByUser(conn, members):
    for member in members:
        tweet_params = 'user_id=' + member['id_str']
        tweet_content = tde.extract_data_from_api(twitter.user_timeline_api, tweet_params)
        if ~(tweet_content is None):
            tweet_content = json.loads(tweet_content)
            for ptweet in tweet_content:
                _tweet = tweet.tweet(ptweet['id_str'], ptweet['text'], ptweet['created_at'], ptweet['entities']['user_mentions'], ptweet, ptweet['user']['id_str'])
                _tweet.storeDatabase(conn)

def extractAllListsByUser(conn, user_id):
    params = 'user_id=' + user_id
    all_lists = tde.extract_data_from_api(twitter.all_lists_api, _search_params=params, _method='GET')
    all_lists = json.loads(all_lists)
    for _list in all_lists:
        t_list = o_list.o_list(_list_id=_list['id_str'], _list_name=_list['name'], _subscriber_count=_list['subscriber_count'], _member_count=_list['member_count'],
                _mode=_list['mode'], _description=_list['description'], _following=_list['following'], _created_at=_list['created_at'],
                _uri=_list['uri'], _creator_id=_list['user']['id_str'], _user_id = user_id, _raw_data=_list)
        t_list.storeDatabase(conn)

def extractAllMembersByList(conn: psycopg_conn, list_ids: List[int]) -> bool:
    for _id in list_ids:
        params = 'list_id=' + _id
        all_members = tde.extract_data_from_api(twitter.all_members_api, _search_params=params, _method='GET')
        all_members = json.loads(all_members)
        for pmember in all_members['users']:
            _member = member.member(_id=pmember['id_str'], _name=pmember['name'], _screen_name=pmember['screen_name'], _location=pmember['location'],
                             _description=pmember['description'], _url=pmember['url'], _raw_data = pmember, _created_at=pmember['created_at'], _list_id=_id)
            _member.storeDatabase(conn)

def extractAllTweetsByList(conn: psycopg_conn, list_ids: List[int]) -> bool:
    for _id in list_ids:
        all_members = user.user().get_all_member_by_list_id(conn, _id)
        for member_id in all_members:
            tweet_params = 'user_id=' + member_id
            all_tweets = tde.extract_data_from_api(twitter.tweet_user_timeline_api, _search_params=tweet_params, _method='GET') 
            all_tweets = json.loads(all_tweets)
            for ptweet in all_tweets:
                _tweet = tweet.tweet(_id=ptweet['id_str'], _text=ptweet['text'], _created_at=ptweet['created_at'], 
                            _user_mentions=ptweet['entities']['user_mentions'], _raw_data = ptweet, _user_id=member_id)
                _tweet.storeDatabase(conn)


if __name__ == '__main__':
    conn = psycopg2.connect(twitter.db_connection)

    _login_user = login_user.login_user()
    _login_user.extract_user_credential()
    _login_user.storeDatabase(conn)
    user_id = _login_user.get_current_login_user_id()
    extractAllListsByUser(conn, user_id)
    
    list_ids = o_list.o_list().get_all_lists_by_user_id(conn, user_id, is_following=True)
    extractAllMembersByList(conn, list_ids)

    extractAllTweetsByList(conn, list_ids)


    # get all lists
    # each lists get all members
    # each members get all tweets






# -- v.2
    # lo_lists = list()
    # all_list = _login_user.extract_all_list()
    # for _list in all_list:
    #     t_list = o_list.o_list(_list_id=_list['id'], _list_name=_list['name'], _subscriber_count=_list['subcriber_count'], _member_count=_list['member_count']
    #     , _mode=_list['mode'], _description=_list['description'], _following=_list['following'], _created_at=_list['created_at'], _uri=_list['uri'],
    #     _creator_id=_list['creator_id'], _user_id=_list['user_id'], _raw_data=_list)
    #     t_list.storeDatabase(conn)
    #     lo_lists.append(t_list)

    # l_members = list()
    # for _list in lo_lists:
    #     all_members = _list.extract_all_members()
    #     for member in all_members:
    #         t_member = user.user(_id=member['id'], _name=member['name'], _screen_name=member['screen_name'], _location=member['location'],
    #             _description=member['description'], _url=member['url'], _raw_data=member, _created_at=member['created_at'])
    #         t_member.storeDatabase(conn)
    #         l_members.append(t_member)

    # for _member in l_members:
    #     _member.extract_all_tweets()
    #     all_tweets = _member.all_members
    #     for tweet in all_tweets:
    #         t_tweet = tweet.tweet(_id = tweet['id'], _text = tweet['text'], _created_at = tweet['created_at'], _user_mentions = tweet['user_mentions'],
    #                                 _raw_data = tweet, _user_id=tweet['user_id'])
    #         t_tweet.storeDatabase(conn)
    
# -- v.1
    # _login_user.extract_all_list()
    # _login_user.save_lists_to_database(conn)

    # for _list in _login_user.all_lists:
    #     if _list.creator_id = _login_user.id:
    #         _list.extract_all_member()
    #         _list.save_members_to_database(conn)
    #         for member in _list.all_members:
    #             member.extract_all_tweets()
    #             member.save_tweets_to_database(conn)

    


    # recent_account = tde.extract_data_from_api(twitter.account_verify_credential_api, _search_params='', _method='GET')
    # print(recent_account)
    # members = getDatatopic(conn, data_topic_id)
    # getTweetByUser(conn, members)