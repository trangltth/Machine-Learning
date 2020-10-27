-- drop function if exists transform_to_12_clock(timestamp);
create or replace function transform_to_12_clock (timestamp)
returns setof timestamp as $$
declare 
    origin_hour integer;
    t_12_lock_hour integer;
    transform_hour integer;
    adding_hour text;
    timestamp_transformation alias for $1;
begin
    origin_hour := (extract(hour from timestamp_transformation))::integer;
    IF origin_hour = 0 then t_12_lock_hour := 12;
        elsif origin_hour > 12 then t_12_lock_hour := (origin_hour % 12);
        else t_12_lock_hour := origin_hour; 
    END IF;
    transform_hour := t_12_lock_hour - origin_hour;
    adding_hour := E'\'' || transform_hour::text || E'hour \'';
    return query execute (concat(E'select (\'', timestamp_transformation ,E'\')::timestamp + interval ', adding_hour));
end;
$$ language plpgsql;