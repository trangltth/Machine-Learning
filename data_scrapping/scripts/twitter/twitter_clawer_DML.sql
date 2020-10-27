--2010-10-18
update users
set is_following = ((raw_data->'following')::text)::boolean;

alter type insert_record_status
add attribute is_updated boolean;

-- 2020-10-17
update users
set created_at = (to_timestamp(trim('"' from (raw_data->'created_at')::text), 'Dy Mon DD HH24:MI:SS US YYYY'))::timestamp;

-- 2020-09-04
update tweets
set user_id = raw_data->'user'->'id';


-- Thu Oct 20 00:24:43 +0000 2016