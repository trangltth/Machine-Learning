from packages.object_scrapping.twitter import user


class member (user.user):
    def __init__ (self, _id='', _name='', _screen_name='', _location='', _description='', _url='', _raw_data='', _created_at='', _list_id=''):
        super().__init__(_id=_id, _name=_name, _location=_location, _screen_name=_screen_name, _description=_description, _url=_url, 
                        _raw_data=_raw_data, _created_at=_created_at)
        self.list_id = _list_id

    def storeDatabase(self, conn):
        cur = conn.cursor()
        try:
            values = (self.id, self.name, self.screen_name, self.location, self.description, self.url, self.raw_data, self.created_at, self.list_id)
            cur.execute('select insert_member(%s, %s, %s, %s, %s, %s, %s, %s, %s)', values)
            conn.commit()
            member_insert_status = cur.fetchall()
            print('member - storeDatabase: ')
            print('action_name - is_existed - member_id - is_inserted - is_updated: ', member_insert_status)
        except Exception as error:
            print('member - storeDatabase: ', error)
            conn.rollback()
        finally:
            cur.close()
            