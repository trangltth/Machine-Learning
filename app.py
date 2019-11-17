from flask import Flask, render_template
import json

app = Flask(__name__)

f = open("tiki_data","r")
data = json.load(f)
# print(data)

all_products = []
all_categories = []

data_category = data['category']
data_product = data['product']

for item in data_category:
    for i in range(len(data_category[item])):
      if(i >= len(all_categories)):
        temp = dict()
        temp[item] = data_category[item][i]
        all_categories.append(temp)
      else:
        all_categories[i][item] = data_category[item][i] 

for item in data_product:
    for i in range(len(data_product[item])):
      if(i >= len(all_products)):
        temp = dict()
        temp[item] = data_product[item][i]
        all_products.append(temp)
      else:
        all_products[i][item] = data_product[item][i] 

@app.route('/')
def index():
    return render_template('index.html', products = all_products, categories = all_categories)

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 