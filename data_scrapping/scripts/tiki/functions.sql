--# 2019-12-04
SELECT OR REPLACE FUNCTION update_product()
RETURN bool AS $$
DECLARE
	detail_ jsonb;
	product_item record;
	products cursor
		FOR SELECT product_id
			FROM (VALUES (14143499), ( 10673986), ( 29165864), ( 29165871), ( 15073958), 
				  ( 3079095), ( 17967705), ( 887617), ( 34391182), ( 29285740), ( 17048907), 
				  ( 34743090), ( 17014269), ( 14143506), ( 4670415), ( 11255703), ( 13170070)) 
			AS temp(product_id);
	BEGIN
		OPEN products;
		LOOP
			FETCH products INTO product_item;
			EXIT WHEN NOT FOUND;
			
			perform detail_ = p.detail::jsonb
			FROM products p
			WHERE p.product_id = product_item.product_id
			LIMIT 1;
			
			UPDATE products
			SET detail = detail_
			WHERE product_id = product_item.product_id;
			
		END LOOP;		
		CLOSE products;
		RETURN true;
END;$$
LANGUAGE plpgsql;

-- 2020-01-13
CREATE OR REPLACE FUNCTION udf_trigger_upsert_categories ()
	RETURNS TRIGGER AS $$
BEGIN 
	IF ((NEW.category_name <> OLD.category_name) 
			OR (NEW.category_link <> OLD.category_link) 
			OR (NEW.parent_id <> OLD.parent_id)
			OR (NEW.is_deleted <> OLD.is_deleted)
			OR OLD.category_id IS NULL)
		THEN
		INSERT INTO categories_log(category_id, category_name, category_link, created_date, is_deleted)
		VALUES(NEW.category_id, NEW.category_name, NEW.category_link, NEW.updated_date, NEW.is_deleted);
	END IF;
	RETURN NEW;
END;$$
LANGUAGE PLPGSQL;

CREATE TRIGGER tr_categories
	AFTER INSERT OR UPDATE OR DELETE
	ON categories
	FOR EACH ROW
	EXECUTE PROCEDURE udf_trigger_categories();

-- 2020-01-21
CREATE OR REPLACE FUNCTION insert_category(
	pcategory_id integer,
	pcategory_name character varying,
	pcategory_link text,
	pparent_id integer)
    RETURNS TABLE(rcategory_id integer, action VARCHAR(20)) 
    LANGUAGE 'plpgsql'
AS $BODY$
DECLARE 
	is_existed BOOL := FALSE;
	is_different BOOL := FALSE;
	is_inserted BOOL := FALSE;
	is_updated BOOL := FALSE;
	rCategory_id INTEGER := 0;
BEGIN		
	is_existed = TRUE
	FROM categories
	WHERE category_id = pCategory_id;

	is_existed = COALESCE(is_existed,FALSE);

	is_different = TRUE
	FROM categories
	WHERE category_id = pCategory_id
		AND (COALESCE(category_name, pCategory_name || 'd') <> COALESCE(pCategory_name, category_name || 'd') 
			OR COALESCE(category_link, PCategory_link || 'd') <> COALESCE(pCategory_link, category_link || 'd')
			OR COALESCE(parent_id, pParent_id + 1) <> COALESCE(pParent_id, parent_id + 1));

	is_different = COALESCE(is_different,FALSE);

	IF NOT(is_existed) THEN
		RETURN QUERY(
			WITH temp(category_id) AS (
				INSERT INTO categories(category_id, category_name, category_link, parent_id)
				VALUES(pCategory_id, pCategory_name, pCategory_link, pParent_id)
				RETURNING category_id
			) 
			SELECT
				category_id, 
				CAST('inserted' AS VARCHAR(20))
			FROM temp
		);
		
	ELSIF is_different THEN
		RETURN QUERY(
			WITH temp AS (
				UPDATE categories
				SET category_name = pCategory_name, category_link = pCategory_link, 
				parent_id = pParent_id, updated_date = CURRENT_TIMESTAMP
				WHERE category_id = pCategory_id
				RETURNING category_id
			)
			SELECT 
				category_id,
				CAST('updated' AS VARCHAR(20))
			FROM temp
		);
		
	END IF;
	
	RETURN;
END;
$BODY$;


-- testing
select insert_category(1801, 'Máy Ảnh - Quay Phim', 'https://tiki.vn/may-anh/c1801?src=c.1801.hamburger_menu_fly_out_banner', null)


---------- Trigger for update Categories
CREATE OR REPLACE FUNCTION udf_trigger_update_categories ()
	RETURNS TRIGGER AS $$
BEGIN 
	IF (COALESCE(NEW.category_name, OLD.category_name || 'd') <> COALESCE(OLD.category_name, NEW.category_name || 'd') 
		OR COALESCE(NEW.category_link, OLD.category_link || 'd') <> COALESCE(OLD.category_link, NEW.category_link || 'd')
		OR COALESCE(NEW.parent_id, OLD.parent_id + 1) <> COALESCE(OLD.parent_id, NEW.parent_id + 1)
		OR NEW.is_deleted <> COALESCE(OLD.is_deleted, NOT(NEW.is_deleted)))

	THEN

		INSERT INTO categories_log(category_id, category_name, category_link, created_date, is_deleted)
		VALUES(OLD.category_id, OLD.category_name, OLD.category_link, OLD.updated_date, OLD.is_deleted);

	END IF;
	RETURN NEW;
END;$$
LANGUAGE PLPGSQL;

DROP TRIGGER IF EXISTS tr_update_categories ON categories;

CREATE TRIGGER tr_update_categories
	AFTER UPDATE
	ON categories
	FOR EACH ROW
	EXECUTE PROCEDURE udf_trigger_update_categories();

---------- Trigger for insert Categories
CREATE OR REPLACE FUNCTION udf_trigger_insert_categories ()
	RETURNS TRIGGER AS $$
BEGIN 
	
	INSERT INTO categories_log(category_id, category_name, category_link, created_date, is_deleted)
	VALUES(NEW.category_id, NEW.category_name, NEW.category_link, NEW.updated_date, NEW.is_deleted);
	RETURN NEW;
END;$$
LANGUAGE PLPGSQL;

DROP TRIGGER IF EXISTS tr_insert_categories ON categories;

CREATE TRIGGER tr_insert_categories
	AFTER UPDATE
	ON categories
	FOR EACH ROW
	EXECUTE PROCEDURE udf_trigger_insert_categories();

--------- Trigger for delete Categories
CREATE OR REPLACE FUNCTION udf_trigger_del_categories ()
	RETURNS TRIGGER AS $$
BEGIN 
	
	INSERT INTO categories_log(category_id, category_name, category_link, created_date, is_deleted)
	VALUES(OLD.category_id, OLD.category_name, OLD.category_link, OLD.updated_date, OLD.is_deleted);
	RETURN OLD;
END;$$		
LANGUAGE PLPGSQL;

DROP TRIGGER IF EXISTS tr_del_categories ON categories;

CREATE TRIGGER tr_del_categories
	AFTER DELETE
	ON categories
	FOR EACH ROW
	EXECUTE PROCEDURE udf_trigger_del_categories();