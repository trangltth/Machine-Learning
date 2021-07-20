import psycopg2, json
from ETL.twitter import twitter_data_extraction as tde
from constants import twitter
from packages.object_scrapping.twitter import o_list, tweet
from typing import List, Dict, Tuple, TypeVar

psycopg_conn = TypeVar('psycopg_conn')

class user:
    def __init__(self, _id='', _name='', _screen_name='', _location='', _description='', _url='', _raw_data='', _created_at='', 
                _is_follower = False, _is_following = False):
        self.id = _id
        self.name = _name
        self.screen_name = _screen_name
        self.location = _location
        self.description = _description
        self.url = _url
        self.raw_data = json.dumps(_raw_data)
        self.created_at = _created_at
        self.is_follower = _is_follower
        self.is_following = _is_following   
    
    def storeDatabase(self, conn):
        cur = conn.cursor()
        try:
            store_values = (self.id, self.name, self.screen_name, self.location, self.description, self.url, self.raw_data, self.created_at, self.is_follower, self.is_following)
            cur.execute('select insert_user(%s::varchar(200), %s, %s, %s, %s, %s, %s, %s, %s, %s);', store_values)
            conn.commit()
            inserted_users = cur.fetchall()
            for user in inserted_users:
                print('is_inserted - user_id - is_existed - is_updated: ', user[0])
        except Exception as error:
            print('storeDatabase function error: ', error)
        finally:
            cur.close()

    def get_all_member_by_list_id(self, conn: psycopg_conn, list_id: str) -> List[id]:
        cur = conn.cursor()
        return_member = []

        try:
            cur.execute('''select user_id from list_user_mapping where is_member='t' and list_id=%s;''', (list_id,))
            all_members = cur.fetchall()
            for member in all_members:
                return_member.append(member[0])
            cur.close()
            return return_member
        except Exception as error:
            print('user - get_all_member_by_list: ', error)
            