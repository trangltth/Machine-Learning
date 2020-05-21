with recursive category_tree (category_id, category_name, level, is_leaf) as (
	select category_id, category_name, 0 as level, 0 as is_leaf
	from categories
	where category_id = 1846
	
	union all
	
	select c.category_id, c.category_name, ct.level+1 as level, case when not exists 
	(select 1 from categories where parent_id = c.category_id) then 1 else 0 end as is_leaf
	from categories c 
		join category_tree ct on c.parent_id = ct.category_id
)
select distinct s.*
from suppliers s
	join supplier_product_mapping spm on spm.supplier_id = s.supplier_id
	join products p on p.product_id = spm.product_id
	join category_product_detail cpd on cpd.product_id = p.product_id
	join category_tree c on c.category_id = cpd.category_id and c.is_leaf = 1