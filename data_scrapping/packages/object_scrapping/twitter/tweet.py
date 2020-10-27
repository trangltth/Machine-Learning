import json
import psycopg2
from constants import twitter

class tweet:
    def __init__(self, _id, _text, _created_at, _user_mentions, _raw_data, _user_id):
      self.tweet_id = _id
      self.text = _text
      self.created_at = _created_at
      self.user_mentions = json.dumps(_user_mentions)
      self.raw_data = json.dumps(_raw_data)
      self.user_id = _user_id

    def storeDatabase(self, conn):
        cur = conn.cursor()
        try:
            tweet_values = (self.tweet_id, self.text, self.created_at, self.user_mentions, self.raw_data, self.user_id)
            cur.execute('select insert_tweet(%s, %s, %s, %s, %s, %s)', tweet_values)
            conn.commit()
            inserted_tweets = cur.fetchall()
            for tweet in inserted_tweets:
                print('is_inserted - tweet_id - is_existed - is_updated', tweet[0])                
        except Exception as error:
            print(error)
            conn.rollback()
        finally:
            cur.close()
        
        