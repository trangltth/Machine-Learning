from urllib.request import urlopen
import requests, urllib.parse
from bs4 import BeautifulSoup
import re, time
from packages.common_libs import common
from packages.object_scrapping import product, supplier 

class category:

  def __init__(self, id_ = -1, category_name = None, category_link = None, parent_id = None):
    self.id_ = id_
    self.category_name = category_name
    self.category_link = category_link
    self.parent_id = parent_id

  # save_type: 0 - Not affect to database
  #            1 - Insert
  #            2 - Update
  def save_db(self, conn):
    type_ = ''
    try:      
      cur = conn.cursor()
      val = (self.id_, self.category_name, self.category_link, self.parent_id)      
      cur.execute("""SELECT insert_category(%s,%s,%s,%s)""", val)
      row_insert = cur.fetchone()      
      
      print('row inserted: ', row_insert)
      if row_insert is not None:
          type_ = re.sub('[\(\)]*','',row_insert[0]).split(',')[1]
      conn.commit() 
      
      

    except Exception as error:
      print("Save_db category:", error)
    finally:
      cur.close()
      return type_

  def update_db(self, conn):
    update_type = 0
    try:      
      cur = conn.cursor()
      val = (self.category_name, self.category_link, self.parent_id, self.id_)
      cur.execute('''UPDATE categories
                  SET category_name = %s, category_link = %s, parent_id = %s, updated_date = CURRENT_TIMESTAMP
                  WHERE category_id = %s
                  returning category_id;''', val)
      row_updated = cur.fetchall()
      
      if len(row_updated) > 0:
        update_type = 2
    except Exception as error:
      print(error)
    finally:
      conn.commit()
      cur.close()
      return update_type
  
  def get_sub_category(self,conn=None):  
    counts = {'inserted':0, 'updated':0}
    try:    
      html = urlopen(self.category_link, timeout=1000)
      bs = BeautifulSoup(html.read(), "html.parser")
      sub_category = bs.find_all("div",{"class":"list-group-item is-child"})
      self.id_ = int(re.sub("[a-z\W\_]*","",bs.select("div.product-listing > script")[0].get_text()))
      

      store_type = self.save_db(conn)
      print(store_type)
      if store_type in counts.keys():
          counts[store_type] += 1

      print(self.id_)
      print(self.category_link)

      # for case page doesn't render list-group-item again
      if (len(sub_category) == 0):
        # self.extract_all_product(conn)
        # supplier.supplier().extract_suppliers_infomation(self.category_link, conn)
        return counts

      # look up in category tree
      for item in sub_category:
        category_data = category()
        category_data.category_name = re.sub("(\([0-9]*\))","",item.select("a")[0].get_text())
        category_data.category_name = re.sub("[\n]*","", category_data.category_name).strip()
        category_link_item = re.sub("(^\/){1}","", item.a['href'])
        category_link_item = common.parse_url(category_link_item)        
        category_data.category_link = "" if item is None else "https://tiki.vn/" +    category_link_item
        category_data.parent_id = self.id_

        # if next page is same category -> final category node -> get product info and save
        if ((category_data.category_link == self.category_link) or (category_data.category_link == "") ):
          # self.extract_all_product(conn)
          # supplier.supplier().extract_suppliers_infomation(self.category_link, conn)
          break
        else:
          store_row = category_data.get_sub_category(conn)  
          for key in store_row.keys():
            counts[key] += store_row[key]
    except Exception as error:
      print('get_sub_category: ', error)
    finally:
      return counts

  def extract_all_product(self, conn):
    try:
      html = urlopen(self.category_link,timeout=1000)
      bs = BeautifulSoup(html.read(),"html.parser")

      box_tag = bs.find_all("div",{"class":"product-listing"})
      max_pages = 0
      
      for item in box_tag:
            script_tag = item.select("div.product-box.no-mg > script")[0].get_text()
            page_info = re.sub("([a-zA-Z\{\}\:\s\;]*)|([a-z\=\s]*)","",script_tag).split(",")
            max_pages = (int(page_info[2]) // int(page_info[1])) + (int(page_info[2]) % int(page_info[1]) > 0)
      
      ### how to know max page???-> when page respone None, raise except and return
      for page in range(1,max_pages+1):
        url_product = self.category_link + "&page=" + str(page)
        self.extract_product(url_product,conn)
      
    except Exception as error:
      print("category - get_all_product: ", error)
      return

  def extract_product(self, url, conn):
    try:
      html = urlopen(url, timeout=1000)
      bs = BeautifulSoup(html.read(), 'html.parser')

      product_ = product.product()
      main_tag = bs.find('div',{"class":"product-box-list"})

      for tag in main_tag.findAll('div',{'class':'product-item'}):
        cover = tag.a.div  
        review_tag = tag.a.select("div.review-wrap > p.review")
        tiki_now_tag = cover.select("p.title")[0].i  
        rating_tag = tag.a.select("div.review-wrap > p.rating > span.rating-content")
        short_title_tag = cover.select("p.title")

        product_.price = cover.select("p.price-sale")[0].span.find(text=True,recursive=False)
        product_.num_review = "0" if len(review_tag) == 0 else review_tag[0].get_text()      
        product_.product_link = tag.a['href']
        product_.short_title = None if (len(short_title_tag) == 0) else re.sub("[\s\\n]*","",short_title_tag[0].get_text())
        product_.tiki_now = 0 if (tiki_now_tag is None) else 1
        product_.title = tag.a['title']
        product_.image = cover.img['src']
        product_.rating = '-1' if (len(rating_tag) == 0) else rating_tag[0].span['style']
        product_.category_id = self.id_
        product_.brand = tag['data-brand']
        product_.product_id = 0 if tag['data-id'] == '' else int(tag['data-id'])
        product_.seller_product_id = 0 if tag['data-seller-product-id'] is None or tag['data-seller-product-id'] == '' else int(tag['data-seller-product-id'])
        product_.clean()
        product_.save_db(conn)

    except Exception as error:
      print("category - get_product:", error)
      
      ## Fake page, return error to break loop
      if main_tag is None: raise error

  def get_parent_category(self, conn):
    cur = conn.cursor()
    cur.execute("SELECT category_id, category_name FROM categories WHERE parent_id IS NULL")
    data = cur.fetchall()
    cur.close()
    return data

  def get_child_category(self,parent_id, conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM categories WHERE parent_id = %s", parent_id)
    categories = cur.fetchall()
    cur.close()
    return categories

  def get_leaf_category_by_root(self, root_category_id, conn):
    cur = conn.cursor()
    cur.execute("""WITH RECURSIVE tree(category_id, category_name, category_link, level_, root, is_leave,
                   path_, category_level_1) AS (
                    SELECT category_id, category_name, category_link, 0 AS level_, 0 AS root, false AS is_leave,
                      CAST(category_name AS TEXT) AS path_,
                      '' AS category_level_1
                    FROM categories
                    WHERE category_id = %s

                    UNION ALL

                    SELECT DISTINCT c.category_id, c.category_name, c.category_link, (t.level_ + 1) AS level_, t.category_id, 
                      CASE WHEN c1.parent_id IS NULL THEN true ELSE false END AS is_leave,
                      CASE WHEN c1.parent_id IS NOT NULL THEN c.category_name || '->' || t.path_ ELSE t.path_ END AS path_,
                      CASE WHEN t.level_ = 0 THEN c.category_name ELSE t.category_level_1 END AS category_level_1
                    FROM categories c
                      JOIN tree t ON t.category_id = c.parent_id
                      -- check if current category has child or not
                      LEFT JOIN categories c1 ON c1.parent_id = c.category_id
                    )
                    SELECT category_id, category_name, category_link, category_level_1
                    FROM tree
                    WHERE is_leave""",(root_category_id,))
    categories = cur.fetchall()
    categories_transform = []
    for category in categories:
      category_dict = dict()
      category_dict['category_id'] = category[0]
      category_dict['category_name'] = category[1]
      category_dict['category_link'] = category[2]
      categories_transform.append(category_dict)

    cur.close()
    return categories_transform

