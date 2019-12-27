import psycopg2

conn = psycopg2.connect("dbname=practicing port=5433 user=postgres")

cur = conn.cursor()

cur.execute("select * from payment")
print(type(cur.fetchall()))