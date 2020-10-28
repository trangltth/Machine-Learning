from packages.object_scrapping.twitter.user import user
from ETL.twitter import twitter_data_extraction as tde
from constants import twitter
import json, psycopg2

class login_user(user):
    def __init__(self, _id='', _name='', _screen_name='', _location='', _description='', _url='', _raw_data='', _created_at='', _is_follower=False, _is_following=False):
        super().__init__(_id=_id, _name=_name, _screen_name=_screen_name, _location=_location, _description=_description, _url=_url, _raw_data=_raw_data,
                    _created_at=_created_at, _is_follower=_is_follower, _is_following=_is_following)
        self.all_list = dict()
    

    def extract_user_credential(self):
        all_information = tde.extract_data_from_api(twitter.account_verify_credential_api, _search_params='')
        all_information = json.loads(all_information)
        self.id = all_information['id_str']
        self.name = all_information['name']
        self.screen_name = all_information['screen_name']
        self.location = all_information['location']
        self.description = all_information['description']
        self.url = all_information['url']
        self.raw_data = json.dumps(all_information)
        self.created_at = all_information['created_at']
    
    def storeDatabase(self, conn):        
        cur = conn.cursor()

        try:
            super().storeDatabase(conn)
            cur.execute('update users set is_login_user = true where user_id = %s returning user_id, user_name;', (self.id,))
            conn.commit()
            user_id_updated = cur.fetchall()
            print('user is updated: ', user_id_updated)
        except Exception as error:
            print('Error when storeDatabase in login_user: ', error)
            conn.rollback()
        finally:
            cur.close()

    def get_current_login_user_id(self):
        return self.id
