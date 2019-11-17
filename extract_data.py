from urllib.request import urlopen
from bs4 import BeautifulSoup
import json


html = urlopen("https://vnexpress.net/")
bs = BeautifulSoup(html.read(), 'html.parser')


titles, images, description = [],[],[]

for tag in bs.findAll('article'):
  try:
    titles.append(tag.a["title"])
    images.append(tag.img["data-original"])
    description.append(tag.p.string)
  except Exception as error:
    pass

f = open("vn_express","w")
data = {'title':titles,'image':images,'description':description}

json.dump(data,f)

f = open("vn_express","r")
data = json.load(f)
for item in data:
  dict("test":data[item][1])