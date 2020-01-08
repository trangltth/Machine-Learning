from requests import get
from static import tiki_information
from packages.object_scrapping import supplier_product_mapping


class supplier_collection:
    
    def __init__(self, supplier_id = 0, supplier_url_slug = ''):
        self.collection_id = 0
        self.collection_name = ''
        self.collection_extra_information = ''
        self.supplier_id = supplier_id
        self.supplier_url_slug = supplier_url_slug

    def extract_supplier_collection(self, conn):
        try:
            all_collections = get(tiki_information.collection_api + str(self.supplier_id)).json()
            for collection in all_collections['data']:
                self.collection_id = collection['id']
                self.collection_name = collection['name']
                self.collection_extra_information = collection
                self.save_to_db(conn)
                self.extract_suppliert_product_mapping(conn)
            
            if(len(all_collections['data']) == 0) :
                self.extract_suppliert_product_mapping(conn)
        except Exception as error:
            print ('extract_supplier_collection', error)

    def extract_suppliert_product_mapping(self, conn):
        supplier_product = supplier_product_mapping.supplier_product_mapping(self.supplier_id, self.collection_id, self.supplier_url_slug)
        supplier_product.extract_supplier_product(conn)

    def save_to_db(self, conn):
        try:
            val = (self.collection_id, self.collection_name, self.supplier_id, self.collection_extra_information)
            cur = conn.cursor()
            cur.execute("""INSERT INTO 
                                    supplier_collections(collection_id, collection_name, supplier_id, collection_extra_information)
                            SELECT temp.collection_id, temp.collection_name, temp.supplier_id, temp.collection_extra_information::jsonb
                            FROM (VALUES (%s, %s, %s, %s)) AS temp(collection_id, collection_name, supplier_id, collection_extra_information)
                                LEFT JOIN supplier_collections sc ON sc.collection_id = temp.collection_id AND
                                                                sc.supplier_id = temp.supplier_id
                            WHERE sc.collection_id IS NULL AND sc.supplier_id IS NULL""", val)
        except Exception as error:
            print('error when save supplier collections: ',error)
        finally:
            conn.commit()
            cur.close()
    
    