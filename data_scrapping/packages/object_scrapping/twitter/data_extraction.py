from ETL.twitter import twitter_data_extraction as tde
from packages.object_scrapping.twitter import user, tweet, login_user, tweet
from constants import twitter
import json, psycopg2

class data_extraction:
    def __init__(self, _params):
        self.params = _params
        self.result_extractions = ''

    def extract_data(self, object_name):
        pass

    def store_result_to_database(self, conn):
        pass

class user_extraction(data_extraction, user):
    def __init__(sefl, user_id):
        super().__init__(user_id)

    def extract_data(self, 'list'):
        all_lists = tde.extract_data_from_api(twitter.all_lists_api, _search_params=self.params, method='GET')
        self.result_extractions = json.loads(all_lists)

    def store_result_to_database(self, conn):
        cur = conn.cursor()
        try:
            values=(self.result_extractions['id_str'], self.result_extractions['list_name'], self.result_extractions['subscriber_count'], self.result_extractions['member_count'],
                self.result_extraction['mode'], self.result_extraction['description'], self.result_extraction['following'], self.result_extractions['uri'],
                self.result_extraction['user']['id_str'], self.params, self.result_extractions)
            cur.execute('select insert_list(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', values)
            conn.commit()
            lists_insert_status = cur.fetchall()
            print('is_existed - list_id - is_inserted - is_updated: ', lists_insert_status)
        except Exception as error:
            print(error)
            conn.rollback()
        finally:
            cur.close()
