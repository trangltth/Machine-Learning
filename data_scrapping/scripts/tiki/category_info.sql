-- 2019-12-03
with recursive tree(category_id, category_name, level_, root, is_leave, path_) as (
select category_id, category_name, 0 as level_, 0 as root, false as is_leave,
	cast(category_name as text) as path_
from categories
where parent_id is null

union all

select distinct c.category_id, c.category_name, (t.level_ + 1) as level_, t.category_id, 
	case when c1.parent_id is null then true else false end as is_leave,
	case when c1.parent_id is not null then c.category_name || '->' || t.path_ else t.path_ end as path_
from categories c
	join tree t on t.category_id = c.parent_id
	-- check if current category has child or not
	left join categories c1 on c1.parent_id = c.category_id
), duplicate_product as(
	select product_id
	from products
	--where detail is not null
	group by product_id
	having count(1) > 1
), info as(
	select p.product_id, t.*
	from duplicate_product dp
		join products p on p.product_id = dp.product_id
		join tree t on t.category_id = p.category_id
	order by p.product_id
)
select *
from info