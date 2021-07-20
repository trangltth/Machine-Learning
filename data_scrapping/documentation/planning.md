##### Working Processing

#### tiwtter database setup (0.5 day)
#### schedule draw data from twitter (0.5day)
    - install R package
    - install cairo
        + depencies: libcairo2 - check which application is using - purpose: change version
    - install pygobject
    - install pygtk-2.24.0
    - install gnome-schedule 
#### python improvement (0.5 day)
#### algorithm (0.5 day)
#### postgres (0.5 day)
#### basic statistics (1 day)
#### data topic analysis (1 day)
#### mongo db (1 day)
#### covid news analysis (3 days) : draw data and analysis
#### profolio website (4 days): research framework -> design -> code


##### 2020-10-28
- commit project to git(working)
- analysis data topic
    + optimize extract data processes for tweet. At present, number of records > 3000 rows, reduce number of tweets store in database everyday. extract data run everyday and get all data for user/tweet/list with insert, update actions
- define more measure fields for tweets and users: follower_counts, favorite_counts

- users table should be inserted from follower and following
- define when a user is deleted: follower and following(friend)

* Tasks:
    - leaning python OOP
    - need to work again with is_follower, is_following - should be define base on business understanding
    - save scheduler information to database:
        + scheduler information
        + scheduler time for users, tweets, lists

##### 2020-10-27
- commit project to git (done) 

- add is_deleted field for lists, users, tweets tables (done)    
    + define when a list/user/tweet is deleted (done)
        + member: get all members -> check if list in database is not exist in data extraction -> delete (done)
        + list: get all lists -> check if list in database is not exist in data extraction -> delete (done)
        + user: follower and following(friend) 

##### 2020-10-21
- List working follow (done)
    + with login user extract all list
    + each lists extract all members
    + each member extract all tweets

##### 2020-10-20
- update insert store procedure users table and tweets table
    + update information if users or tweets are updated (done)
    + add is_following, is_follower to insert_user store procedure (done)
- add lists table, list_users table (done)
    + define database diagram (done)
    + running data for lists table (done)
        + adding is_login_user into users table (done)
        + add login_user_id for all table (skip)


##### 2020-10-18
- Dislay content of compiste type: insert_record_status (done)

##### 2020-10-17
- change default current_date to current_timestamp (exists)
- add inserted_at, updated_at, created_at for users table (done)
- add is_follower, is_following columns into users tables (done)
- update insert store procedure users table and tweets table:
    + update information if users or tweets are updated
- add lists table, list_users table

##### 2020-10-16
- searching for IT sholarships (pending)
    + Conditions 
- Job looking

##### 2020-10-14
- configure file can set specific version of package when it runs?
    + No
- there is imposible to install multi version for a package (task)
    + how to install multi version <- apt install can do
    + working for glib-2.29.92

##### 2020-09-07
- install R package
- install cairo
    + depencies: libcairo2 - check which application is using - purpose: change version
- install pygobject
- install pygtk-2.24.0
- install gnome-schedule 

- business: how to increasing tweets for Data topic?

##### 2020-09-04
- add user_id column into tweets table (done)
- run ETL functions to update data (done)
- design to make daily running ETL jobs 

##### 2020-09-01

??? how to know users dataset is enough to continue analysis Data topic
- Estimated time: 4.2 days (evening 01st - 04th-09-2020)
- evening 01st: What are main sharings of each followers in Data topic?

additional tasks:
- how does Toward Data science works?

##### 2020-08-30
- Data topic analysis

##### 2020-08-29
- insert users data
- insert tweets data by users

##### 2020-08-19
- importing members and tweets in Data list (working)
    + get tweets by users: filter by user, location
