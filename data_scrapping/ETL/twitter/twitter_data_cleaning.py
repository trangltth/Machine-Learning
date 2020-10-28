import codecs, base64
from ETL.twitter import twitter_data_extraction as te
from urllib.parse import quote_plus
from constants import twitter
import json, psycopg2
from string import Formatter

def clean_list_table_by_user_id(conn, extract_list, user_id):
    extract_list = tuple(extract_list)
    cur = conn.cursor()
    try:
        cur.execute('''update list_user_mapping 
                        set is_deleted = true, deleted_at = current_timestamp 
                        where user_id = %s and list_id not in %s and is_deleted = 'f'
                        returning list_id, user_id;''', (user_id, extract_list))
        conn.commit()
        list_user_deleted = cur.fetchall()
        print('list_user_mapping are deleted: ', list_user_deleted)

        cur.execute('''update lists
                        set is_deleted = 't', deleted_at = current_timestamp
                        where creator_id = %s and list_id not in %s and (is_deleted is null or is_deleted = 'f')
                        returning list_id, creator_id;''', (user_id, extract_list))
        conn.commit()
        list_deleted = cur.fetchall()
        print('lists are deleted: ', list_deleted)
    except Exception as error:
        print('Error - twitter_data_cleaning - clean_list_table_by_user_id: ', error)
        conn.rollback()
    finally:
        cur.close()

def update_member_list(conn, member_list, list_id):
    cur = conn.cursor()
    member_list = tuple(member_list)
    try:
        cur.execute('''update list_user_mapping
                    set is_deleted = 't' and deleted_at = current_timestamp
                    where list_id = %s and user_id not in %s and is_member = 'f' and (is_deleted is null or is_deleted = 'f')
                        and (is_creator is null or is_creator = 'f') and (is_follower is null or is_follower = 'f')
                    returning list_id, user_id;''', (list_id, member_list))
        conn.commit()
        members_deleted = cur.fetchall()
        print('members are deleted: ', members_deleted)
    except Exception as error:
        print('Error - update_member_list: ', error)
        conn.rollback()
    finally:
        cur.close()
