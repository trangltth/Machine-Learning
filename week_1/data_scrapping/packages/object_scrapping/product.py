from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import json, re, unicodedata
from packages.common_libs import common

class product:

  def __init__(self, title="", image="", price=0, description="", short_title="", product_link = "",
          tiki_now=0, num_review=None, rating=0.0, brand = "", category_id = 0, product_id = 0):
    self.title = title
    self.image = image
    self.price = price
    self.description = description
    self.short_title = short_title
    self.product_link = product_link
    self.tiki_now = tiki_now
    self.num_review = num_review
    self.rating = rating
    self.brand = brand
    self.category_id = category_id
    self.product_id = product_id
    self.detail = ""

  def save_db(self, conn):   
    try:
      cur = conn.cursor()

      # There are some products belong to multi category
      # if product already exists -> don't insert
      if(not self.get_product_by_id(conn)):
        # insert into products table
        val = (self.product_id, self.title, self.price, self.image, self.short_title, 
        self.product_link, bool(self.tiki_now), self.num_review, self.rating, self.brand)
        print("product info: ", val)
        cur.execute("""insert into products(product_id, title, price, image, short_title, product_link,
                    tiki_now, review, rating, brand)
                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", val)
        conn.commit()

      # insert into category_product_detail table
      if (not self.get_category_by_id(conn)):
        val = (self.product_id, self.category_id)
        cur.execute("""insert into category_product_detail(product_id, category_id)
                    values(%s,%s)""", val)
        conn.commit()

    except Exception as error:
      print("product - save_db:", error)      
    finally:
      cur.close()

  def clean(self):
    self.title = re.sub("[\\n\\\]","",self.title)
    self.price = re.sub("[đ\s\.]*", "", self.price)
    self.num_review = int(re.sub("([\(\)])|(nhận xét)*","",self.num_review))
    self.rating = int(re.sub("(width:)|(\%)","",self.rating))/100
    self.product_link = re.search("(.*\.html)", self.product_link).group(0)

  def get_all_product_by_category(self, category_id, conn):
    cur = conn.cursor()
    cur.execute("""with recursive tree(category_id, category_name, level_, root) as (
                      select category_id, category_name, 0 as level_, 0 as root
                      from categories
                      where category_id = %s

                      union all

                      select c.category_id, c.category_name, (t.level_ + 1) as level_, t.category_id
                      from categories c
                        join tree t on t.category_id = c.parent_id
                      )
                      select category_id
                      from tree
                      where category_id not in (select distinct root from tree)""", (category_id,))
    all_categories = tuple(cur.fetchall())
    cur.execute("""select p.product_id as product_id, p.title as title, p.price as price, p.image as image, 
                        p.short_title as short_title, p.product_link as product_link, p.tiki_now as tiki_now,
                        p.review as review, p.rating as rating, p.brand as brand, p.detail as detail,
                        cpd.category_id as category_id 
                  from category_product_detail cpd
                  join products p on p.product_id = cpd.product_id  where cpd.category_id in %s;"""
                       , (all_categories,))
    data = cur.fetchall()
    cur.close()
    return data

  def extract_all_product_detail(self, category_id, conn):
    try:
      list_products = self.get_all_product_by_category(category_id,conn)
    
      for product_item in list_products:
        product_ = product()
        product_.product_id = product_item[0]
        product_.category_id = product_item[10]
        product_.product_link = product_item[5]
        product_.extract_product_detail()
        product_.save_detail_to_db(conn)
    except Exception as error:
      print(error)
    
  def extract_product_detail(self):
    try:
      html = urlopen(self.product_link)
      bs = BeautifulSoup(html.read(),"html.parser")

      product_detail = bs.find("table",{"id":"chi-tiet"})

      product_detail_data = dict()
      for tr_tag in product_detail.tbody.find_all("tr", recursive = False):
        td_tags = tr_tag.find_all("td", recursive = False)

        # clean data
        attribute = common.strip_accents(str(td_tags[0].string).strip().lower())
        value = common.strip_accents(str(td_tags[1].get_text()).strip().lower())
        
        # transform data
        attribute = attribute.replace(" ", "_")
        value = re.sub("\n"," ",value)
        product_detail_data[attribute] = value

      self.detail = product_detail_data
    except Exception as error:
      print(error)
    
  def save_detail_to_db(self, conn):
    try:
      cur = conn.cursor()
      val = (json.dumps(self.detail), self.product_id)
      cur.execute("""Update products set detail = %s where product_id = %s """, val)
      print(val)
    except Exception as error:
      print(error)
    finally:
      conn.commit()
      cur.close()  

  def get_product_by_id(self, conn):
    cur = conn.cursor()
    cur.execute('select * from products where product_id = %s', (self.product_id,))
    product_info = cur.fetchone()
    cur.close()

    return product_info

  def get_category_by_id(self, conn):
    cur = conn.cursor()
    cur.execute("""select * from category_product_detail where category_id = %s and product_id = %s""",
              (self.category_id, self.product_id))
    category_info = cur.fetchone()
    cur.close()
    
    return category_info


