from flask import Flask, render_template
import json

app = Flask(__name__)

f = open("tiki_data","r")
data = json.load(f)
# print(data)

all_products = []
all_categories = []

all_categories = data['category']

for item in data:
    for i in range(len(data[item])):
      if(i >= len(all_products)):
        temp = dict()
        temp[item] = data[item][i]
        all_products.append(temp)
      else:
        all_products[i][item] = data[item][i] 

@app.route('/')
def index():
    return render_template('index.html', products = all_products, categories = all_categories)

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 