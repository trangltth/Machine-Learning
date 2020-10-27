from requests import get
from constants import tiki_information
import re
from packages.object_scrapping import supplier_collection

class supplier_product_mapping:
    def __init__(self, supplier_id = 0, collection_id = 0, supplier_url_slug = ''):
        self.supplier_id = supplier_id
        self.collection_id = collection_id        
        self.supplier_url_slug = supplier_url_slug
        self.product_id = 0
        self.extra_information = ''

    def extract_supplier_product(self, conn):
        try:
            if self.collection_id == 0:
                link = re.sub("url_slug",self.supplier_url_slug,tiki_information.prodoct_without_collection_api)
                all_products = get(link).json()
            else:
                all_products = get(tiki_information.product_collection_api + str(self.collection_id)).json()
            
            for product in all_products['data']:
                self.product_id = product['id']
                self.extra_information = product
                self.save_to_db(conn)
        except Exception as error:
            print("extract_supplier_product: ", error)

    def save_to_db(self, conn):
        try:
            cur = conn.cursor()
            val = (self.supplier_id, self.collection_id, self.product_id, self.extra_information)
            # cur.execute("""insert into 
            #                     supplier_product_mapping(supplier_id, collection_id, product_id, product_extra_information)
            #                 select temp.supplier_id, temp.collection_id, temp.product_id, temp.product_extra_information::jsonb
            #                 from (values(%s, %s, %s, %s)) as temp(supplier_id, collection_id, product_id, product_extra_information)
            #                     left join supplier_product_mapping as s on s.supplier_id = temp.supplier_id 
            #                                                             and s.collection_id = temp.collection_id
            #                                                             and s.product_id = temp.product_id	
            #                 where s.supplier_id is null and s.collection_id is null and s.product_id is null""", val)
            cur.execute("""insert into 
                            supplier_product_mapping(supplier_id, collection_id, product_id, product_extra_information)
                            values(%s, %s, %s, %s)""", val)
        except Exception as error:
            print("error when saving to supplier_product_mapping: ", error)
        finally:            
            conn.commit()
            cur.close()

    