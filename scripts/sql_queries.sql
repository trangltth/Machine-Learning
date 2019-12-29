CREATE TABLE products(
  product_id INTEGER , 
  title TEXT, 
  price MONEY, 
  image TEXT, 
  short_title VARCHAR(255), 
  sub_category_link VARCHAR(500),
  tiki_now BOOL, 
  review VARCHAR(255), 
  rating NUMERIC(2,1),
  brand VARCHAR(500),
  category_id INTEGER,
  PRIMARY KEY (product_id, category_id));

CREATE TABLE categories(
  category_id INTEGER PRIMARY KEY, 
  category_name VARCHAR(500),
  parent_id INTEGER);

ALTER TABLE products 
  ADD COLUMN detail json;

#-- 2019-12-03

CREATE TABLE category_product_detail(
  category_id INTEGER,
  product_id INTEGER,
  created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(product_id, category_id)
);

-- Copy products data into category_product_detail

insert into category_product_detail(product_id, category_id)
SELECT product_id, category_id
from products;

ALTER TABLE category_product_detail
  ALTER COLUMN updated_date SET DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE category_product_detail
  ALTER COLUMN created_date SET DEFAULT CURRENT_TIMESTAMP;

CREATE TABLE IF NOT EXISTS products_temp
AS
  SELECT DISTINCT product_id, title, price, image, short_title, 
          substring(sub_category_link from '.*html') as sub_category_link, 
          tiki_now, review, rating, brand, detail::jsonb, CURRENT_TIMESTAMP as created_date
          , CURRENT_TIMESTAMP as updated_date
  FROM products;

--# 2019-12-04
alter table products
rename to products_archived

alter table products_temp
rename to products

alter table products
	add primary key (product_id)

alter table category_product_detail
  add CONSTRAINT pk_product_id FOREIGN KEY (product_id) REFERENCES products(product_id),
  add CONSTRAINT pk_category_id FOREIGN KEY (category_id) REFERENCES categories(category_id);

alter table products
  rename COLUMN sub_category_link
    to product_link;
