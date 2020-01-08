import pandas as pd
from  ETL_jobs import extract_all_category, extract_all_products_from_category, extract_category_infomation
import psycopg2, unicodedata
from psycopg2 import extras
import sys, static.tiki_information as tiki_info

conn = psycopg2.connect(tiki_info.db_connection)
url_category = "https://tiki.vn/"
psycopg2.extensions.register_adapter(dict, psycopg2.extras.Json)

if __name__ == "__main__":
  # extract_all_category(url_category, conn)
  ### Get product detail base on product_link
  # extract_all_products_from_category(1846,conn)
  #  https://tiki.vn/laptop-may-vi-tinh-linh-kien/c1846?_lc=Vk4wMzkwMjIwMDk%3D&src=c.1846.hamburger_menu_fly_out_banner
  extract_category_infomation("Laptop - Máy Vi Tính - Linh Kiện","https://tiki.vn/laptop-may-vi-tinh-linh-kien/c1846?_lc=Vk4wMzkwMjIwMDk%3D&src=c.1846.hamburger_menu_fly_out_banner",conn)
  
  conn.close()
  
