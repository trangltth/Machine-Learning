from urllib.request import urlopen
from bs4 import BeautifulSoup
import json, re
from packages.object_scrapping import product, category


def extract_all_category(url,conn):
    html_main = urlopen(url, timeout=1000)
    bs_main = BeautifulSoup(html_main.read(), 'html.parser')
    categories_tag = bs_main.find("ul",{"class":"Navigation__Wrapper-s3youc-0 hWakax"})

    for category_item in categories_tag.findAll("li"):
      category_data = category.category()
      category_data.category_link = category_item.a['href']
      category_data.category_name = category_item.select("span.text")[0].get_text()
      category_data.get_sub_category(conn)

def extract_category_detail(name, url, conn):
    category_data = category.category()
    category_data.category_link = url
    category_data.category_name = name
    category_data.get_sub_category(conn)

def extract_all_products_from_category(category_id, conn):
    product.product().extract_all_product_detail(category_id,conn)
