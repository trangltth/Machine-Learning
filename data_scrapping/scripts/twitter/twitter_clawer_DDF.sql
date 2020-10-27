-- 2020-10-27
create table action_statuses (
    action_name varchar(200),
    action_statuses insert_record_status
);

--2020-10-25
create type table_action_status as(
    action_name varchar(200),
    action_status insert_record_status
);

-- 2020-10-20
create table list_user_mapping(
    list_id varchar(200),
    user_id varchar(200),
    is_creator boolean,
    is_follower boolean,
    is_member boolean,
    is_deleted boolean,
    created_at timestamp,
    updated_at timestamp default current_timestamp,
    inserted_at timestamp default current_timestamp,
    deleted_at timestamp,
    primary key(list_id, user_id),
    foreign key (list_id) references lists(list_id),
    foreign key (user_id) references users(user_id)
);

create table lists_log(
    list_log_id serial,
    list_id varchar(200),
    list_name varchar(200),
    subscriber_count integer,
    member_count integer,
    mode varchar(50),
    description text,
    created_at timestamp,
    uri varchar(200),
    creator_id varchar(200),
    raw_data jsonb,
    is_deleted boolean,
    inserted_at timestamp,
    updated_at timestamp,
    deleted_at timestamp,
    date_log_at timestamp default current_timestamp,
    primary key(list_log_id),
    foreign key (list_id) references lists(list_id),
    foreign key (creator_id) references users(user_id)
);

create table lists(
    list_id varchar(200),
    list_name varchar(200),
    subscriber_count integer,
    member_count integer,
    mode varchar(50),
    description text,
    created_at timestamp,
    uri varchar(200),
    creator_id varchar(200),
    raw_data jsonb,
    is_deleted boolean,
    inserted_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp,
    deleted_at timestamp,
    primary key(list_id),
    foreign key(creator_id) references users(user_id)
);

-- 2020-10-18
create table users_log(
    user_log_id serial,
    user_id varchar(200),
    user_name varchar(100),
    screen_name varchar(100),
    location varchar(200),
    description text,
    url varchar(200),
    raw_data jsonb,
    created_at timestamp,
    inserted_at timestamp,
    updated_at timestamp,
    date_log_at timestamp,
    is_follower boolean,
    is_following boolean,
    primary key (user_log_id)
);

create table tweets_log(
    tweet_log_id serial,
    tweet_id varchar(200),
    text text,
    user_mentions jsonb,
    raw_data jsonb,
    user_id varchar(200),
    created_at timestamp,
    updated_at timestamp,
    inserted_at timestamp,
    date_log_at timestamp,
    primary key(tweet_log_id)
);


-- 2020-10-17
alter table users
add column inserted_at timestamp default current_timestamp,
add column updated_at timestamp default current_timestamp,
add column created_at timestamp,
add column is_follower boolean default false,
add column is_following boolean default false;

-- 2020-09-04
alter table tweets
add column user_id varchar(200);

alter table tweets
add foreign key(user_id) references users(user_id);

-- 2020-08-28
create type insert_record_status as(
    is_existed boolean,
    is_inserted boolean,
    record_id varchar(200)
);  

create table tweets(
    tweet_id varchar(200),
    text text,
    user_mentions jsonb,
    raw_data jsonb,
    created_at timestamp,
    updated_at timestamp default current_timestamp,
    inserted_at timestamp default current_timestamp,
    primary key(tweet_id)
);

-- 2020-08-22
create table users(
    user_id varchar(200),
    user_name varchar(100),
    screen_name varchar(100),
    location varchar(200),
    description text,
    url varchar(200),
    raw_data jsonb,
    primary key (user_id)
);

-- 2020-08-20
CREATE TABLE cities(
    city_id VARCHAR(20),
    city_name VARCHAR(100),
    city_name_ascii varchar(100),
    latidue numeric(6,4),
    longidue numeric(7,4),
    country varchar(100),
    iso2 varchar(2),
    iso3 varchar(3),
    admin_name varchar(100),
    capital varchar(15),
    population numeric(20,1),
    primary key (city_id)
);

copy cities(city_name, city_name_ascii, latidue, longidue, country, iso2, iso3, admin_name,capital, population, city_id)
from '/home/trang/working/projects/Machine-Learning/data_scrapping/dataset/worldcities.csv'
with (format 'csv',  header True, force_null (population));