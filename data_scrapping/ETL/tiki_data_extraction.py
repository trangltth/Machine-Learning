from urllib.request import urlopen
from bs4 import BeautifulSoup
import json, re, constants.tiki_information as tiki_info
from packages.object_scrapping import product, category
import threading, math, time, sys, psycopg2, sys, multiprocessing, pickle
from multiprocessing import Pool, current_process

counts = {'inserted': 0, 'updated': 0}
all_threads = []
sys.setrecursionlimit(2000)

# def extract_all_category_v_thread(url,conn):    
    
#     start = time.time()

#     html_main = urlopen(url, timeout=tiki_info.url_open_timeout)
#     bs_main = BeautifulSoup(html_main.read(), 'html.parser')
#     categories_tag = bs_main.find("ul",{"class":"Navigation__Wrapper-s3youc-0 hWakax"})        

#     all_categories = categories_tag.findAll("li")
#     categories_num = len(all_categories)
#     threads_num = 3

#     groups_num = math.floor(categories_num / threads_num)
#     modules_num = categories_num % threads_num
#     global all_threads
#     all_threads = []

#     for idx in range(groups_num):
#         idx_real = idx * threads_num
#         threads = []
#         all_threads = []
#         for i in range(threads_num):
#             thread = threading.Thread(target=extract_category_info,args=(conn, all_categories[idx_real + i]), daemon=True)
#             threads.append(thread)
#             all_threads.append(thread)
#             thread.start()

#         for thread in threads:
#             thread.join()
    
#     threads = []
#     all_threads = []

#     for idx in range(modules_num):
#         idx_real = (groups_num * 3) + idx 
        
#         threading_ = threading.Thread(target=extract_category_info,args=(conn, all_categories[idx_real]))
#         threading_.start()
#         threads.append(threading_)
#         all_threads.append(threading_)

#     for thread in threads:
#         thread.join()

#     end = time.time()
#     print('Time for scrapping: ', round((end - start)/60,2))

#     return counts



def extract_content_category(category_id, category_name, conn):
    category_data = category.category()
    category_data.category_id = category_id
    category_data.category_name = category_name
    categories_leaf = category_data.get_leaf_category_by_root(category_id, conn)
    for category_item in categories_leaf:
        print(category_item)

def extract_all_products_from_category(category_id, conn):
    product.product().extract_all_product_detail(category_id,conn)

def extract_category_info(conn, category_item, idx ):
    print('start extract data from thread: ', idx)
    if conn == 0:
        conn = psycopg2.connect(tiki_info.db_connection)

    global counts

    category_data = category.category()
    category_data.category_link = category_item.a['href']
    category_data.category_name = category_item.select("span.text")[0].get_text()
    stored_row = category_data.get_sub_category(conn)
    
    for key in stored_row.keys():
            counts[key] += stored_row[key]

def lock_thread(lock):
    lock.acquire()

current_pool = ''

def extract_all_category(url,conn):    
    
    start = time.time()

    html_main = urlopen(url, timeout=tiki_info.url_open_timeout)
    bs_main = BeautifulSoup(html_main.read(), 'html.parser')
    categories_tag = bs_main.find("ul",{"class":"Navigation__Wrapper-s3youc-0 hWakax"})        

    all_categories = categories_tag.findAll("li")
    categories_num = len(all_categories)
    threads_num = 3

    groups_num = math.floor(categories_num / threads_num)
    modules_num = categories_num % threads_num
    global current_pool

    # for idx in range(groups_num):
    #     idx_real_1 = (idx * 3)
    #     idx_real_2 = (idx * 3) + 1
    #     idx_real_3 = (idx * 3) + 2
    #     with Pool(processes=3) as pool:
    #         current_pool = pool
    #         pool.starmap(extract_category_info, [(0, all_categories[idx_real_1], idx_real_1), (0, all_categories[idx_real_2], idx_real_2), (0, all_categories[idx_real_3], idx_real_3)])
    #         pool.close()
    #         pool.join()

    # for idx in range(modules_num):
    #     idx_real =  idx#(groups_num*3) + idx

    #     with Pool(processes=1) as pool:
    #         current_pool = pool
    #         pool.starmap(extract_category_info, [(0, all_categories[idx_real], idx_real)])
    #         pool.close()
    #         pool.join()
    time.sleep(20)
    end = time.time()
    print('Time for scrapping: ', round((end - start)/60,2))

    return counts

def test(a):
    print('test: ', a)

# To do: run test 
def pause_jobs():
    try:
        print('start exit')
        global current_pool       
        current_pool.close()
        return True
    except Exception as error:
        print('error while pause job: ', error)
        return False
    

if __name__ == '__main__':
    conn = psycopg2.connect(tiki_info.db_connection)
    extract_all_category(tiki_info.tiki_url, conn)
    conn.close()
