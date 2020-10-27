from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from requests import get
from constants import tiki_information as tiki_info
from packages.object_scrapping import supplier_collection

class supplier:
    
    def __init__(self, supplier_id = 0, supplier_name = '', category_link = ''):
        self.supplier_id = 0
        self.supplier_name = ''
        self.category_link = ''
        self.detail = ''
        self.collection = None
        self.url_slug = ''

    def clean(self):
        self.supplier_name = re.sub('[\(,0-9,\),\n]*',"",self.supplier_name)
        self.supplier_name = str.strip(self.supplier_name).lower()

    def extract_suppliers_infomation(self, link, conn):
        try:
            html = urlopen(link, timeout=tiki_info.url_open_timeout)
            bs = BeautifulSoup(html.read(), 'html.parser')

            suppliers_main_tag = bs.find('div',{'id':'collapse-seller'})

            for supplier_tag in suppliers_main_tag.findAll('div', {'class':'list-group-item'}):
                if sum(extend_class in supplier_tag['class'] for extend_class in ['list-group-show','list-group-hide']) > 0:
                    continue
                supplier_processing = supplier()
                id_attribute = supplier_tag.a['data-filter-value']
                supplier_processing.supplier_id = int(id_attribute)
                supplier_processing.supplier_name = supplier_tag.a.get_text()
                detail = get(tiki_info.supllier_api + id_attribute).json()
                supplier_processing.detail = detail
                supplier_processing.url_slug = detail['url_slug']
                supplier_processing.clean()
                supplier_processing.save_to_db(conn)
                supplier_processing.extract_collections(conn)
        except Exception as error:
            print('extract_suppliers_infomation: ', error)
            if (suppliers_main_tag is None):
                print(link, ' do not have any external supplier')
                return

    def extract_collections(self, conn):
        collections = supplier_collection.supplier_collection(self.supplier_id, self.url_slug)
        collections.extract_supplier_collection(conn)
    
    def save_to_db(self, conn):
        try:
            cur = conn.cursor()
            val = (self.supplier_id, self.supplier_name, self.detail)

            cur.execute("""INSERT INTO 
                            suppliers(supplier_id, supplier_name, supplier_extra_information) 
                        SELECT temp.supplier_id, temp.supplier_name, temp.supplier_extra_information::json
                        FROM (VALUES(%s, %s, %s)) AS temp(supplier_id, supplier_name, supplier_extra_information)
                            LEFT JOIN suppliers s ON s.supplier_id = temp.supplier_id
                        WHERE s.supplier_id IS NULL""", val)
        except Exception as error:
            print('Error when supplier save to db: ', error)
        finally:
            conn.commit()
            cur.close()

    def get_all_supplier(self, conn):
        try:
            cur = conn.cursor()
            cur.execute("""select supplier_id, supplier_name 
                            from suppliers""")
            all_suppliers = cur.fetchAll()
            return all_suppliers
        except Exception as error:
            print(error)
        finally:
            cur.close()

