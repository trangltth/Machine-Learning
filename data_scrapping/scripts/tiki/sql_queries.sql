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

-- 2019-12-03

CREATE TABLE category_product_detail(
  category_id INTEGER,
  product_id INTEGER,
  created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(product_id, category_id)
);

-- Copy products data into category_product_detail

INSERT INTO category_product_detail(product_id, category_id)
SELECT product_id, category_id
FROM products;

ALTER TABLE category_product_detail
  ALTER COLUMN updated_date SET DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE category_product_detail
  ALTER COLUMN created_date SET DEFAULT CURRENT_TIMESTAMP;

CREATE TABLE IF NOT EXISTS products_temp
AS
  SELECT DISTINCT product_id, title, price, image, short_title, 
          SUBSTRING(sub_category_link FROM '.*html') as sub_category_link, 
          tiki_now, review, rating, brand, detail::jsonb, CURRENT_TIMESTAMP as created_date
          , CURRENT_TIMESTAMP as updated_date
  FROM products;

-- 2019-12-04
ALTER TABLE products
rename TO products_archived

ALTER TABLE products_temp
rename TO products

ALTER TABLE products
	ADD PRIMARY KEY (product_id)

ALTER TABLE category_product_detail
  ADD CONSTRAINT pk_product_id FOREIGN KEY (product_id) REFERENCES products(product_id),
  ADD CONSTRAINT pk_category_id FOREIGN KEY (category_id) REFERENCES categories(category_id);

ALTER TABLE products
  rename COLUMN sub_category_link
    TO product_link;


ALTER TABLE products OWNER TO trang;
ALTER TABLE products_archived OWNER TO trang;
ALTER TABLE categories OWNER TO trang;
ALTER TABLE category_product_detail OWNER TO trang;
ALTER TABLE suppliers OWNER TO trang;

-- 2020-01-05
--PATTERN: 
-- TABLE suppliers(
--   supplier_id INTEGER,
--   supplier_name VARCHAR(5000),
--   supplier_extra_information jsonb,
--   PRIMARY KEY (supplier_id)
-- );

ALTER TABLE suppliers
  DROP COLUMN url,
  ADD COLUMN supplier_extra_information jsonb;

CREATE TABLE supplier_collections(
  collection_id INTEGER,
  collection_name VARCHAR(5000),
  supplier_id INTEGER,
  collection_extra_information jsonb,
  PRIMARY KEY (collection_id, supplier_id)
);

CREATE TABLE supplier_product_mapping(
  supplier_id INTEGER,
  product_id INTEGER,
  collection_id INTEGER,
  product_extra_information jsonb,
  PRIMARY KEY(supplier_id, product_id, collection_id)
);

-- 2020-01-07
ALTER TABLE products
ADD COLUMN seller_product_id INTEGER DEFAULT 0;

ALTER TABLE suppliers
ADD COLUMN created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE supplier_collections
ADD COLUMN created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE supplier_product_mapping
ADD COLUMN created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

CREATE TABLE products_log(
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
  created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (product_id, category_id));


-- 2020-01-13

ALTER TABLE categories
  ADD COLUMN category_link text,
  ADD COLUMN is_deleted BOOLEAN DEFAULT FALSE,
  ADD COLUMN created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  ADD COLUMN updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

CREATE TABLE categories_log(
  category_log_id SERIAL,
  category_id INTEGER,
  category_name VARCHAR(500),
  category_link TEXT,
  parent_id INTEGER,
  created_date TIMESTAMP,
  is_deleted BOOLEAN,
  created_date_log TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(category_log_id)
);

INSERT INTO categories_log(category_id, category_name, category_link, parent_id, is_deleted, created_date)
SELECT category_id, category_name, category_link, parent_id, is_deleted, updated_date
FROM categories;





