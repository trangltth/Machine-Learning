from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

html_main = urlopen("https://tiki.vn/")
bs_main = BeautifulSoup(html_main.read(), 'html.parser')

categories_tag = bs_main.find("ul",{"class":"Navigation__Wrapper-s3youc-0 hWakax"})

product_link, category_name = [],[]

for category in categories_tag.findAll("li"):
  product_link.append(category.a['href'])
  category_name.append(category.select("span.text")[0].get_text())

# Todo: merge product and category

html = urlopen("https://tiki.vn/dien-thoai-may-tinh-bang/c1789?src=c.1789.hamburger_menu_fly_out_banner")
bs = BeautifulSoup(html.read(), 'html.parser')


titles, images, price, description = [],[],[],[]
short_title, sub_category, tiki_now, review, rating = [],[],[],[],[]

main_tag = bs.find('div',{"class":"product-box-list"})

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

data = {"product":{"title":titles, "price": price, "image":images, 
"short_title":short_title, "sub_category":sub_category, "tiki_now":tiki_now, "review":review,
"rating": rating}, "category":{"product_link": product_link, "category_name":category_name}}

file = open("tiki_data","w")

json.dump(data,file)
