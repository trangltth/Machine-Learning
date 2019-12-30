--# 2019-12-04
create or replace function update_product()
returns bool as $$
Declare
	detail_ jsonb;
	product_item record;
	products cursor
		for select product_id
			from (values (14143499), ( 10673986), ( 29165864), ( 29165871), ( 15073958), 
				  ( 3079095), ( 17967705), ( 887617), ( 34391182), ( 29285740), ( 17048907), 
				  ( 34743090), ( 17014269), ( 14143506), ( 4670415), ( 11255703), ( 13170070)) 
			as temp(product_id);
	begin
		open products;
		loop
			fetch products into product_item;
			exit when not found;
			
			perform detail_ = p.detail::jsonb
			from products p
			where p.product_id = product_item.product_id
			limit 1;
			
			update products
			set detail = detail_
			where product_id = product_item.product_id;
			
		end loop;		
		close products;
		return true;
end;$$
language plpgsql;