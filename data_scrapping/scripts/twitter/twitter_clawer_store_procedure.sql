-- Store procedure: insert_member
-- Parameters: member_id, member_name, screen_name, location, description, url, raw_data, created_at, list_id
-- Parameter types: varchar(200), varchar(100), varchar(100), varchar(200), text, varchar(200), jsonb, timestamp, varchar(200)
-- Description: insert members into list_user_mapping table, users table
drop function if exists insert_member;
create function insert_member(varchar(200), varchar(100), varchar(100), varchar(200), text, varchar(200), jsonb, timestamp, varchar(200))
returns setof table_action_status
as $$
declare
    list_user_mapping_insert_status insert_record_status;
    user_insert_status insert_record_status;
    pmember_id alias for $1;
    pmember_name alias for $2;
    pscreen_name alias for $3;
    plocation alias for $4;
    pdescription alias for $5;
    purl alias for $6;
    praw_data alias for $7;
    pcreated_at alias for $8;
    plist_id alias for $9;
begin
    user_insert_status = insert_user(pmember_id, pmember_name, pscreen_name, plocation, pdescription, purl, praw_data, pcreated_at, false, false);

    list_user_mapping_insert_status.is_inserted = false;
    list_user_mapping_insert_status.is_updated = false;
    list_user_mapping_insert_status.record_id = pmember_id;

    list_user_mapping_insert_status.is_existed = true
                from list_user_mapping
                where list_id = plist_id and user_id = pmember_id and is_member ='t';

    list_user_mapping_insert_status.is_existed = coalesce(list_user_mapping_insert_status.is_existed, false);

    if not(list_user_mapping_insert_status.is_existed)
    then
        list_user_mapping_insert_status.is_inserted = true;

        insert into list_user_mapping(list_id, user_id, is_creator, is_follower, is_member, created_at)
        select plist_id, pmember_id, false, false, true, pcreated_at;

    end if;

    return query select action_name, return_statuses
            from 
                (values('insert user'::varchar(200), user_insert_status), ('insert list_user_mapping'::varchar(200), list_user_mapping_insert_status)) as return_values(action_name, return_statuses);
 
end
$$ language plpgsql;

-- select insert_member('1', 'Data Science', 'DataScience', 'US', 'Data Science', 'Data Science', '{"id": 1}'::jsonb, (current_timestamp)::timestamp, '130385922');


--store procedure: insert_user
--parameters: user_id, user_name, screen_name, location, description, url, raw_data, created_a, is_follower, is_following
--parameter type: varchar(200), varchar(100), varchar(100), varchar(200), text, varchar(200), jsonb, timestamp, boolean, boolean
--description: add user to users table
-- Date Modified            Content
-- 2020-10-20               remove cte when update users table and insert users_log table

drop function if exists insert_user;
create function insert_user(varchar(200), varchar(100), varchar(100), varchar(200), text, varchar(200), jsonb, timestamp, boolean, boolean) 
returns insert_record_status
as $$
declare
    is_inserted boolean default 0;
    is_existed boolean default 0;
    is_updated boolean default 0;
    puser_id alias for $1;
    puser_name alias for $2;
    pscreen_name alias for $3;
    plocation alias for $4;
    pdescription alias for $5;
    purl alias for $6;
    praw_data alias for $7;
    pcreated_at alias for $8;
    pis_follower alias for $9;
    pis_following alias for $10;
begin
    is_existed := 1
    from users
    where user_id = puser_id;

    is_existed := coalesce(is_existed,0::boolean);

    if not (is_existed)
    then 
        is_inserted = 1;    
        insert into users(user_id, user_name, screen_name, location, description, url, raw_data, created_at, is_follower, is_following)
        values (puser_id, puser_name, pscreen_name, plocation, pdescription, purl, praw_data, pcreated_at, pis_follower, pis_following);

    else
        is_updated = 1
            from users
            where user_id = puser_id and (raw_data != praw_data or is_follower != pis_follower or is_following != pis_following);

        is_updated = coalesce(is_updated, false);

        if (is_updated)
        then
            insert into users_log(user_id, user_name, screen_name, location, description, url, raw_data, inserted_at, updated_at, created_at, date_log_at, is_follower, is_following)
            select user_id, user_name, screen_name, location, description, url, raw_data, inserted_at, updated_at, created_at, current_timestamp, is_follower, is_following
            from users
            where user_id = puser_id;

            update users
            set user_name = puser_name, screen_name = pscreen_name, location = plocation, description = pdescription,
                url = purl, raw_data = praw_data, created_at = pcreated_at, is_follower = pis_follower, is_following = pis_following,
                updated_at = current_timestamp
            where user_id = puser_id;            
        end if;

    end if;

    return row(is_inserted, puser_id::varchar(200), is_existed, is_updated);
end;
$$ language plpgsql;

-- Store procedure: insert_list
-- Parameters: list_id, list_name, subscriber_count, member_count, mode, description, following, created_at, uri, creator_id, raw_data
-- Parameter datatype: varchar(200), varchar(200), integer, integer, varchar(50), text, boolean, timestamp, varchar(200), varchar(200), jsonb
-- Description: insert list into list table
-- Date Modified            Content
drop function if exists insert_list;
create function insert_list(varchar(200), varchar(200), integer, integer, varchar(50), text, boolean, timestamp, varchar(200), varchar(200), jsonb, varchar(200))
returns insert_record_status
as $$
declare
    is_inserted boolean default false;
    is_existed boolean default false;
    is_updated boolean default false;
    is_creator boolean default false;
    plist_id alias for $1;
    plist_name alias for $2;
    psubscriber_count alias for $3;
    pmember_count alias for $4;
    pmode alias for $5;
    pdescription alias for $6;
    pfollowing alias for $7;
    pcreated_at alias for $8;
    puri alias for $9;
    pcreator_id alias for $10;
    praw_data alias for $11;
    puser_id alias for $12;
begin
    is_existed = 1
            from lists
            where list_id = plist_id;
            
    is_existed = coalesce(is_existed, false);

    if puser_id = pcreator_id
    then 
        is_creator = true;
    end if;

    if not (is_existed)
    then
        is_inserted = 1;

        insert into lists(list_id, list_name, subscriber_count, member_count, mode, description, created_at, uri, creator_id, 
                    raw_data, is_deleted)
        select plist_id, plist_name, psubscriber_count, pmember_count, pmode, pdescription, pcreated_at, puri, 
            pcreator_id, praw_data, false;

        insert into list_user_mapping(list_id, user_id, is_creator, is_follower, is_member, is_deleted, created_at)
        select plist_id, puser_id, is_creator, pfollowing, false, false, pcreated_at;

    else
    -- list_name, subscriber_count, member_count, mode, description, following, created_at, uri - all these fields are extracted from raw data
        is_updated = true
                from lists
                where list_id = plist_id and (raw_data != praw_data);

        is_updated = coalesce(is_updated, false);
        
        if is_updated
        then
            insert into lists_log(list_id, list_name, subscriber_count, member_count, mode, description, created_at, uri, creator_id, 
            raw_data, inserted_at, updated_at, is_deleted, deleted_at)
            select list_id, list_name, subscriber_count, member_count, mode, description, created_at, uri, creator_id, raw_data, inserted_at,
                    updated_at, is_deleted, deleted_at
            from lists
            where list_id = plist_id;

            update lists
            set list_name = plist_name, subscriber_count = psubscriber_count, member_count = pmember_count, mode = pmode, description = pdescription, 
                created_at = pcreated_at, uri = puri, creator_id = pcreator_id, raw_data = praw_data, updated_at = current_timestamp
            where list_id = plist_id;

        end if;
    end if;

    return row(is_existed, plist_id::varchar(200), is_inserted, is_updated);

end;
$$ language plpgsql;

-- select insert_list('1'::varchar(200), 'data'::varchar(200), 0, 30, 'public'::varchar(50), 'pratice01'::text, true, current_timestamp::timestamp, ''::varchar(200), '1'::varchar(200), ('{}')::jsonb, '2'::varchar(200));

--store procedure: insert_user
--parameters: user_id, user_name, screen_name, location, description, url, raw_data, created_a, is_follower, is_following
--parameter type: varchar(200), varchar(100), varchar(100), varchar(200), text, varchar(200), jsonb, timestamp, boolean, boolean
--description: add user to users table
-- Date Modified            Content
-- 2020-10-20               remove cte when update users table and insert users_log table

drop function if exists insert_user;
create function insert_user(varchar(200), varchar(100), varchar(100), varchar(200), text, varchar(200), jsonb, timestamp, boolean, boolean) 
returns insert_record_status
as $$
declare
    is_inserted boolean default 0;
    is_existed boolean default 0;
    is_updated boolean default 0;
    puser_id alias for $1;
    puser_name alias for $2;
    pscreen_name alias for $3;
    plocation alias for $4;
    pdescription alias for $5;
    purl alias for $6;
    praw_data alias for $7;
    pcreated_at alias for $8;
    pis_follower alias for $9;
    pis_following alias for $10;
begin
    is_existed := 1
    from users
    where user_id = puser_id;

    is_existed := coalesce(is_existed,0::boolean);

    if not (is_existed)
    then 
        is_inserted = 1;    
        insert into users(user_id, user_name, screen_name, location, description, url, raw_data, created_at, is_follower, is_following)
        values (puser_id, puser_name, pscreen_name, plocation, pdescription, purl, praw_data, pcreated_at, pis_follower, pis_following);
    else
        is_updated = 1
            from users
            where user_id = puser_id and (user_name != puser_name or screen_name != pscreen_name
                    or location != plocation or description != pdescription or url != purl or raw_data != praw_data
                    or created_at != pcreated_at or is_follower != pis_follower or is_following != pis_following);

        is_updated = coalesce(is_updated, false);

        if (is_updated)
        then
            insert into users_log(user_id, user_name, screen_name, location, description, url, raw_data, inserted_at, updated_at, created_at, date_log_at, is_follower, is_following)
            select user_id, user_name, screen_name, location, description, url, raw_data, inserted_at, updated_at, created_at, current_timestamp, is_follower, is_following
            from users
            where user_id = puser_id;

            update users
            set user_name = puser_name, screen_name = pscreen_name, location = plocation, description = pdescription,
                url = purl, raw_data = praw_data, created_at = pcreated_at, is_follower = pis_follower, is_following = pis_following,
                updated_at = current_timestamp
            where user_id = puser_id;            
        end if;

    end if;

    return row(is_inserted, puser_id::varchar(200), is_existed, is_updated);
end;
$$ language plpgsql;

-- begin;
--     select insert_user('1'::varchar(200), 'test_@'::varchar(100), 'test'::varchar(100), 'test'::varchar(200), 'test'::text, 'test'::varchar(200), '{"id": 1}'::jsonb, ('2020-10-18 23:25:59.977987')::timestamp, false, false);
-- end;

-- Store procedure: insert_tweet
-- Parameters: tweet_id, text, created_at, user_mentions, raw_data, user_id
-- Data types: varchar(200), text, timestamp, jsonb, jsonb, varchar(200)
-- Description: insert tweet into tweets table
-- Date-Modified                Content
-- 2020-10-19                   Change updating block from cte to using transaction

drop function if exists insert_tweet;
create function insert_tweet(varchar(200), text, timestamp, jsonb, jsonb, varchar(200))
returns insert_record_status
as $$
<<fn>>
declare
    is_inserted boolean default 0;
    is_existed boolean default 0;
    is_updated boolean default 0;
    ptweet_id alias for $1;
    ptext alias for $2;
    pcreated_at alias for $3;
    puser_mentions alias for $4;
    praw_data alias for $5;
    puser_id alias for $6;
begin
    is_existed = 1
    from tweets
    where tweet_id = ptweet_id;

    is_existed = coalesce(is_existed, 0::boolean);

    if not (is_existed)
    then
        is_inserted = 1;
        insert into tweets(tweet_id, text, created_at, user_mentions, raw_data, user_id)
        values(ptweet_id, ptext, pcreated_at, puser_mentions, praw_data, puser_id);
    else
        is_updated = 1
            from tweets
            where tweet_id = ptweet_id and
                (text != ptext or user_mentions != puser_mentions or raw_data != praw_data or user_id != puser_id or created_at != pcreated_at);
        
        is_updated = coalesce(is_updated, false);

        if (is_updated)
        then
            insert into tweets_log(tweet_id, text, user_mentions, raw_data, user_id, inserted_at, updated_at, created_at, date_log_at)
            select tweet_id, text, user_mentions, raw_data, user_id, inserted_at, updated_at, created_at, current_timestamp
            from tweets
            where tweet_id = ptweet_id;

            update tweets
            set text = ptext, user_mentions = puser_mentions, raw_data = praw_data, user_id = puser_id, updated_at = current_timestamp,
                created_at = pcreated_at
            where tweet_id = ptweet_id;
        end if;

    end if;

    return row(is_inserted, ptweet_id::varchar(200), is_existed, is_updated);

end;
$$ language plpgsql;

--  select insert_tweet('13'::varchar(200), 'testing_4qw'::text, ('2020-10-20 09:30:00.88426')::timestamp, ('{ "id": "1", "text": "testing"}')::jsonb, ('{"id":"1", "text": "testing"}')::jsonb, '1'::varchar(200));

select insert_tweet('12'::varchar(200), 'testing_4q'::text, current_timestamp::timestamp, ('{ "id": "1", "text": "testing"}')::jsonb, ('{"id":"1", "text": "testing"}')::jsonb, '1'::varchar(200));

-- 2020-10-18
-- store procedure
-- description: update when user information is changed
drop function if exists insert_user;
create function insert_user(varchar(200), varchar(100), varchar(100), varchar(200), text, varchar(200), jsonb, timestamp, boolean, boolean) 
returns insert_record_status
as $$
declare
    is_inserted boolean default 0;
    is_existed boolean default 0;
    is_updated boolean default 0;
    puser_id alias for $1;
    puser_name alias for $2;
    pscreen_name alias for $3;
    plocation alias for $4;
    pdescription alias for $5;
    purl alias for $6;
    praw_data alias for $7;
    pcreated_at alias for $8;
    pis_follower alias for $9;
    pis_following alias for $10;
begin
    is_existed := 1
    from users
    where user_id = puser_id;

    is_existed := coalesce(is_existed,0::boolean);

    if not (is_existed)
    then 
        is_inserted = 1;    
        insert into users(user_id, user_name, screen_name, location, description, url, raw_data, created_at, is_follower, is_following)
        values (puser_id, puser_name, pscreen_name, plocation, pdescription, purl, praw_data, pcreated_at, pis_follower, pis_following);
    else
        is_updated = 1
            from users
            where user_id = puser_id and (user_name != puser_name or screen_name != pscreen_name
                    or location != plocation or description != pdescription or url != purl or raw_data != praw_data
                    or created_at != pcreated_at or is_follower != pis_follower or is_following != pis_following);

        is_updated = coalesce(is_updated, false);

        with user_temp(user_id, user_name, screen_name, location, description, url, raw_data, inserted_at, updated_at, created_at, is_follower, is_following) as (
            update users
            set user_name = puser_name, screen_name = pscreen_name, location = plocation, description = pdescription,
                url = purl, raw_data = praw_data, created_at = pcreated_at, is_follower = pis_follower, is_following = pis_following,
                updated_at = current_timestamp
            where user_id = puser_id and (user_name != puser_name or screen_name != pscreen_name 
                or location != plocation or description != pdescription or url != purl or raw_data != praw_data
                or created_at != pcreated_at or is_follower != pis_follower or is_following != pis_following)
            returning user_id, user_name, screen_name, location, description, url, raw_data, inserted_at, updated_at, created_at, is_follower, is_following
        )
            insert into users_log(user_id, user_name, screen_name, location, description, url, raw_data, inserted_at, updated_at, created_at, date_log_at, is_follower, is_following)
            select user_id, user_name, screen_name, location, description, url, raw_data, inserted_at, updated_at, created_at, current_timestamp, is_follower, is_following
            from user_temp;
    end if;

    return row(is_inserted, puser_id::varchar(200), is_existed, is_updated);
end;
$$ language plpgsql;


-- select insert_user('1'::varchar(200), 'test_@'::varchar(100), 'test'::varchar(100), 'test'::varchar(200), 'test'::text, 'test'::varchar(200), '{"id": 1}'::jsonb, ('2020-10-18 23:25:59.977987')::timestamp, false, false);

-- 2020-10-18
-- store procedure
-- describse: add updating when the tweet is existed
drop function if exists insert_tweet_v2;
create function insert_tweet_v2(varchar(200), text, timestamp, jsonb, jsonb, varchar(200))
returns insert_record_status
as $$
<<fn>>
declare
    returning_status insert_record_status;
    ptweet_id alias for $1;
    ptext alias for $2;
    pcreated_at alias for $3;
    puser_mentions alias for $4;
    praw_data alias for $5;
    puser_id alias for $6;
begin

    returning_status = row(false, '0'::varchar(200), false, false);

    returning_status.is_existed = 1
    from tweets
    where tweet_id = ptweet_id;

    returning_status.is_existed = coalesce(returning_status.is_existed, 0::boolean);

    if not (returning_status.is_existed)
    then
        returning_status.is_inserted = 1;
        insert into tweets(tweet_id, text, created_at, user_mentions, raw_data, user_id)
        values(ptweet_id, ptext, pcreated_at, puser_mentions, praw_data, puser_id);
    else        
        returning_status.is_updated = 1
            from tweets
            where tweet_id = ptweet_id and 
                    (text != ptext or user_mentions != puser_mentions or raw_data != praw_data or user_id != puser_id or created_at != pcreated_at);

        returning_status.is_updated = coalesce(returning_status.is_updated, false);

        with tweet_temp(tweet_id, text, user_mentions, raw_data, user_id, inserted_at, updated_at, created_at) 
        as (
            update tweets
            set text = ptext, user_mentions = puser_mentions, raw_data = praw_data, user_id = puser_id, updated_at = current_timestamp,
                created_at = pcreated_at
            where tweet_id = ptweet_id and 
                    (text != ptext or user_mentions != puser_mentions or raw_data != praw_data or user_id != puser_id or created_at != pcreated_at)
            returning tweet_id, text, user_mentions, raw_data, user_id, inserted_at, updated_at, created_at
        )
        insert into tweets_log(tweet_id, text, user_mentions, raw_data, user_id, inserted_at, updated_at, created_at, date_log_at)
        select tweet_id, text, user_mentions, raw_data, user_id, inserted_at, updated_at, created_at, current_timestamp
        from tweet_temp;
    end if;

    return returning_status;

end;
$$ language plpgsql;

-- 2020-10-18
-- store procedure
-- describse: add updating when the tweet is existed
drop function if exists insert_tweet;
create function insert_tweet(varchar(200), text, timestamp, jsonb, jsonb, varchar(200))
returns insert_record_status
as $$
<<fn>>
declare
    is_inserted boolean default 0;
    is_existed boolean default 0;
    is_updated boolean default 0;
    ptweet_id alias for $1;
    ptext alias for $2;
    pcreated_at alias for $3;
    puser_mentions alias for $4;
    praw_data alias for $5;
    puser_id alias for $6;
begin
    is_existed = 1
    from tweets
    where tweet_id = ptweet_id;

    is_existed = coalesce(is_existed, 0::boolean);

    if not (is_existed)
    then
        is_inserted = 1;
        insert into tweets(tweet_id, text, created_at, user_mentions, raw_data, user_id)
        values(ptweet_id, ptext, pcreated_at, puser_mentions, praw_data, puser_id);
    else   
        is_updated = 1
            from tweets
            where tweet_id = ptweet_id and
                (text != ptext or user_mentions != puser_mentions or raw_data != praw_data or user_id != puser_id or created_at != pcreated_at);
        
        is_updated = coalesce(is_updated, false);

        with tweet_temp(tweet_id, text, user_mentions, raw_data, user_id, inserted_at, updated_at, created_at) 
        as (
            update tweets
            set text = ptext, user_mentions = puser_mentions, raw_data = praw_data, user_id = puser_id, updated_at = current_timestamp,
                created_at = pcreated_at
            where tweet_id = ptweet_id and 
                    (text != ptext or user_mentions != puser_mentions or raw_data != praw_data or user_id != puser_id or created_at != pcreated_at)
            returning tweet_id, text, user_mentions, raw_data, user_id, inserted_at, updated_at, created_at
        )
            insert into tweets_log(tweet_id, text, user_mentions, raw_data, user_id, inserted_at, updated_at, created_at, date_log_at)
            select tweet_id, text, user_mentions, raw_data, user_id, inserted_at, updated_at, created_at, current_timestamp
            from tweet_temp;
    end if;

    return row(is_inserted, ptweet_id::varchar(200), is_existed, is_updated);

end;
$$ language plpgsql;

--  select insert_tweet('12'::varchar(200), 'testing_4'::text, current_timestamp::timestamp, ('{ "id": "1", "text": "testing"}')::jsonb, ('{"id":"1", "text": "testing"}')::jsonb, '1'::varchar(200));

-- 2020-09-22
-- store procedure
-- describse: updating insert tweets
drop function if exists insert_tweet;
create function insert_tweet(varchar(200), text, timestamp, jsonb, jsonb, varchar(200)) returns insert_record_status
as $$
declare
    is_inserted boolean default 0;
    is_existed boolean default 0;
    ptweet_id alias for $1;
    ptext alias for $2;
    pcreated_at alias for $3;
    puser_mentions alias for $4;
    praw_data alias for $5;
    puser_id alias for $6;
begin
    is_existed = 1
    from tweets
    where tweet_id = ptweet_id;

    is_existed = coalesce(is_existed, 0::boolean);

    if not (is_existed)
    then
        is_inserted = 1;
        insert into tweets(tweet_id, text, created_at, user_mentions, raw_data, user_id)
        values(ptweet_id, ptext, pcreated_at, puser_mentions, praw_data, puser_id);
    end if;

    return row(is_inserted, ptweet_id::varchar(200), is_existed);

end;
$$ language plpgsql;


-- 2020-08-29
-- store procedure
-- describse: insert tweets
drop function if exists insert_tweet;
create function insert_tweet(varchar(200), text, timestamp, jsonb, jsonb) returns insert_record_status
as $$
declare
    is_inserted boolean default 0;
    is_existed boolean default 0;
    ptweet_id alias for $1;
    ptext alias for $2;
    pcreated_at alias for $3;
    puser_mentions alias for $4;
    praw_data alias for $5;
begin
    is_existed = 1
    from tweets
    where tweet_id = ptweet_id;

    is_existed = coalesce(is_existed, 0::boolean);

    if not (is_existed)
    then
        is_inserted = 1;
        insert into tweets(tweet_id, text, created_at, user_mentions, raw_data)
        values(ptweet_id, ptext, pcreated_at, puser_mentions, praw_data);
    end if;

    return row(is_inserted, ptweet_id::varchar(200), is_existed);

end;
$$ language plpgsql;



-- 2020-08-27
-- store procedure
-- describse: insert users
drop function if exists insert_user;
create function insert_user(varchar(200), varchar(100), varchar(100), varchar(200), text, varchar(200), jsonb) returns insert_record_status
as $$
declare
    is_inserted boolean default 0;
    is_existed boolean default 0;
    puser_id alias for $1;
    puser_name alias for $2;
    pscreen_name alias for $3;
    plocation alias for $4;
    pdescription alias for $5;
    purl alias for $6;
    praw_data alias for $7;
begin
    is_existed := 1
    from users
    where user_id = puser_id;

    is_existed := coalesce(is_existed,0::boolean);

    if not (is_existed)
    then 
        is_inserted = 0;    
        insert into users(user_id, user_name, screen_name, location, description, url, raw_data)
        values (puser_id, puser_name, pscreen_name, plocation, pdescription, purl, praw_data);
    else
        is_inserted := 1;
    end if;

    return row(is_inserted, puser_id::varchar(200), is_existed);
end;
$$ language plpgsql;