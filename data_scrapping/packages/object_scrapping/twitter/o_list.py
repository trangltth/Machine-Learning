import psycopg2, json
from ETL.twitter import twitter_data_extraction as tde
from constants import twitter
from packages.object_scrapping.twitter import user
from typing import List, Dict, Tuple, TypeVar

psycopg_conn = TypeVar('psycopg_conn')

class o_list:
    def __init__(self, _list_id = '', _list_name = '', _subscriber_count=0, _member_count=0, _mode='public', _description='', _following=True, 
            _created_at='', _uri='', _creator_id='', _user_id='', _raw_data=''):
        self.list_id = _list_id
        self.list_name = _list_name
        self.subscriber_count = _subscriber_count
        self.member_count = _member_count
        self.mode = _mode
        self.description = _description
        self.following = _following
        self.created_at = _created_at
        self.uri = _uri
        self.creator_id = _creator_id
        self.raw_data = json.dumps(_raw_data)
        self.user_id = _user_id
        self.all_members = ''


    def storeDatabase(self, conn):
        cur = conn.cursor()
        try:
            values = (self.list_id, self.list_name, self.subscriber_count, self.member_count, self.mode, self.description, self.following, 
            self.created_at, self.uri, self.creator_id, self.raw_data, self.user_id)     
            cur.execute('select insert_list(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', values)
            conn.commit()
            inserted_lists = cur.fetchall()
            for inserted_list in inserted_lists:
                print('o_list - storeDatabase: is_existed - list_id - is_inserted - is_updated', inserted_list)
        except Exception as error:
            print('StoreDatabase in o_list: ' , error)
            conn.rollback()
        finally:
            cur.close()

    def get_all_lists_by_user_id(self, conn: psycopg_conn, user_id: int, is_following: bool) -> List[int]:
        cur = conn.cursor()
        try:
            cur.execute('''select distinct l.list_id
                                from lists l 
                                    join list_user_mapping lum 
                                    on lum.list_id = l.list_id 
                                where lum.user_id = %s and is_follower='t';''', (user_id,))
            all_lists = cur.fetchall()
            return_list = []
            for _list in all_lists:
                return_list.append(_list[0])
            cur.close()
            return return_list
        except Exception as error:
            print('o_list - get_all_list_by_user_id: ', error)
            
