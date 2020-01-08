from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from packages.object_scrapping import product, supplier

class category:

  def __init__(self, id_ = -1, category_name = None, category_link = None, parent_id = None):
    self.id_ = id_
    self.category_name = category_name
    self.category_link = category_link
    self.parent_id = parent_id

  def save_db(self, conn):
    try:
      cur = conn.cursor()
      val = (self.id_, self.category_name, self.parent_id)
      cur.execute("""insert into categories(category_id, category_name, parent_id) 
                    select temp.category_id, temp.category_name, cast(temp.parent_id as int)
                      from (values(%s,%s,%s)) as temp(category_id, category_name, parent_id)
                          left join categories c on c.category_id = temp.category_id
                          where c.category_id is null;""", val)
    except Exception as error:
      print("Save_db category:", error)
    finally:
      conn.commit()  
      cur.close()

  def get_sub_category(self,conn=None):  
    html = urlopen(self.category_link, timeout=1000)
    bs = BeautifulSoup(html.read(), "html.parser")
    sub_category = bs.find_all("div",{"class":"list-group-item is-child"})
    self.id_ = int(re.sub("[a-z\W\_]*","",bs.select("div.product-listing > script")[0].get_text()))
    self.save_db(conn)

    # for case page doesn't render list-group-item again
    if (len(sub_category) == 0):
      self.extract_all_product(conn)
      supplier.supplier().extract_suppliers_infomation(self.category_link, conn)
      return

    # look up in category tree
    for item in sub_category:
      category_data = category()
      category_data.category_name = re.sub("(\([0-9]*\))","",item.select("a")[0].get_text())
      category_data.category_link = "" if item is None else "https://tiki.vn/" + item.a['href']       
      category_data.parent_id = self.id_

      # if next page is same category -> final category node -> get product info and save
      if ((category_data.category_link == self.category_link) or (category_data.category_link == "") ):
        self.extract_all_product(conn)
        supplier.supplier().extract_suppliers_infomation(self.category_link, conn)
        break
      else:
        category_data.get_sub_category(conn)  

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
    cur.execute("select * from categories where parent_id is null")
    data = cur.fetchall()
    cur.close()
    return data

  def get_child_category(self,parent_id, conn):
    cur = conn.cursor()
    cur.execute("select * from categories where parent_id = %s", parent_id)
    categories = cur.fetchall()
    cur.close()
    return categories

  def get_leaf_category_by_root(self, root_category_id, conn):
    cur = conn.cursor()
    cur.execute("""with recursive tree(category_id, category_name, level_, root, is_leave,
                   path_, category_level_1) as (
                    select category_id, category_name, 0 as level_, 0 as root, false as is_leave,
                      cast(category_name as text) as path_,
                      '' as category_level_1
                    from categories
                    where category_id = %s

                    union all

                    select distinct c.category_id, c.category_name, (t.level_ + 1) as level_, t.category_id, 
                      case when c1.parent_id is null then true else false end as is_leave,
                      case when c1.parent_id is not null then c.category_name || '->' || t.path_ else t.path_ end as path_,
                      case when t.level_ = 0 then c.category_name else t.category_level_1 end as category_level_1
                    from categories c
                      join tree t on t.category_id = c.parent_id
                      -- check if current category has child or not
                      left join categories c1 on c1.parent_id = c.category_id
                    )
                    select category_id, category_level_1
                    from tree
                    where is_leave""",(root_category_id,))
    category_id_list = cur.fetchall()
    cur.close()
    return category_id_list





