from urllib.request import urlopen
from bs4 import BeautifulSoup
import json


html = urlopen("https://tiki.vn/dien-thoai-may-tinh-bang/c1789?src=c.1789.hamburger_menu_fly_out_banner")
bs = BeautifulSoup(html.read(), 'html.parser')


category, titles, images, price, description = [],[],[],[],[]
short_title, sub_category, tiki_now, review, rating = [],[],[],[],[]

main_tag = bs.find('div',{"class":"product-box-list"})
category.append(main_tag["data-impress-list-title"])

for tag in main_tag.findAll('div',{'class':'product-item'}):
  cover = tag.a.div  
  review_tag = tag.a.select("div.review-wrap > p.review")
  tiki_now_tag = cover.select("p.title")[0].i
  
  sub_category.append(tag["data-category"])
  short_title.append(cover.select("p.title")[0].get_text())
  tiki_now.append(""if (tiki_now_tag is None) else tiki_now_tag['class'][0])
  titles.append(tag.a['title'])
  price.append(cover.select("p.price-sale")[0].span.find(text=True,recursive=False))
  images.append(cover.img['src'])
  review.append("" if len(review_tag) == 0 else review_tag[0].get_text())
  rating.append(tag.a.select("div.review-wrap > p.rating > span.rating-content")[0].span['style'])

data = {"category": category, "title":titles, "price": price, "image":images, 
"short_title":short_title, "sub_category":sub_category, "tiki_now":tiki_now, "review":review,
"rating": rating}

file = open("tiki_data","w")

json.dump(data,file)

file = open("tiki_data","r")

data_read = json.load(file)

# for item in data_read:
#   print(data_read)