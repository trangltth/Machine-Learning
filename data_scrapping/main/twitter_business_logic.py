import sys
sys.path.append('/home/trang/working/projects/Machine-Learning/data_scrapping')
from ETL.twitter import twitter_data_cleaning as tdc, twitter_data_extraction as tde
from constants import twitter
from packages.object_scrapping.twitter import user, tweet, login_user, o_list, member
import json, psycopg2
from datetime import datetime
from typing import List, Dict, Tuple, TypeVar

psycopg_conn = TypeVar('psycogp_conn')

def extractAllListsByUser(conn: psycopg_conn, user_id: int) -> None: 
    params = 'user_id=' + user_id
    all_lists = tde.extract_data_from_api(twitter.all_lists_api, _search_params=params, _method='GET')
    all_lists = json.loads(all_lists)
    extracted_list = []
    for _list in all_lists:
        t_list = o_list.o_list(_list_id=_list['id_str'], _list_name=_list['name'], _subscriber_count=_list['subscriber_count'], _member_count=_list['member_count'],
                _mode=_list['mode'], _description=_list['description'], _following=_list['following'], _created_at=_list['created_at'],
                _uri=_list['uri'], _creator_id=_list['user']['id_str'], _user_id = user_id, _raw_data=_list)
        t_list.storeDatabase(conn)
        extracted_list.append(_list['id_str'])
    
    tdc.clean_list_table_by_user_id(conn, extracted_list, user_id)

    # collection of lists map with user_id
    # list_user_mapping: user_id, list_id
    # mark (user_id, list_id) = deleted when list_id not in collection of lists

def extractAllMembersByList(conn: psycopg_conn, list_ids: List[int]) -> bool:
    for _id in list_ids:
        params = 'list_id=' + _id
        all_members = tde.extract_data_from_api(twitter.all_members_api, _search_params=params, _method='GET')
        all_members = json.loads(all_members)
        member_ids = []
        for pmember in all_members['users']:
            _member = member.member(_id=pmember['id_str'], _name=pmember['name'], _screen_name=pmember['screen_name'], _location=pmember['location'],
                             _description=pmember['description'], _url=pmember['url'], _raw_data = pmember, _created_at=pmember['created_at'], _list_id=_id)
            _member.storeDatabase(conn)
            member_ids.append(pmember['id_str'])
        tdc.update_member_list(conn, member_ids, _id)

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