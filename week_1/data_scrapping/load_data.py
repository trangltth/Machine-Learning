import pandas as pd
from  ETL_jobs import extract_all_category, extract_all_products_from_category, extract_category_detail
import psycopg2, unicodedata
import sys

conn = psycopg2.connect("dbname=postgres port=5433 user=postgres")
url_category = "https://tiki.vn/"


if __name__ == "__main__":
  # extract_all_category(url_category, conn)
  ### Get product detail base on product_link
  # extract_all_products_from_category(1846,conn)
  # extract_category_detail("nha_sach_tiki","https://tiki.vn/nha-sach-tiki/c8322?src=c.8322.hamburger_menu_fly_out_banner",conn)
  conn.close()

