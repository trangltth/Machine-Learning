import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.insert(1,"e:\\projects\\machine_learning\\week_1\\data_scrapping")
from packages.object_data import category

conn = psycopg2.connect("dbname=postgres port=5433 user=postgres")

cur = conn.cursor()

categories = tuple(category.category().get_leaf_category_by_root(1846,conn))

cur.execute("""select p.product_id, p.title, p.price, p.tiki_now, p.brand, p.detail 
                from products p
                    join category_product_detail cpd
                        on p.product_id = cpd.product_id
                where cpd.category_id in %s""", (categories,))

data = cur.fetchall()
cur.close()
conn.close()

print(len(categories))
