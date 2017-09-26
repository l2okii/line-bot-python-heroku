import os
import psycopg2
import urlparse

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)


# conn = psycopg2.connect(
#     "dbname='mylocaldb' user='postgres' host='localhost' password=''"
# )

def select_test():
    sql = """SELECT * from l2ig_db;"""
    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            print ' ', row

        cur.close()
    finally:
        if conn is not None:
            conn.close()


def insert_test(line_id,wallet_id):
    sql = """INSERT INTO l2ig_db(line_id,wallet_id) VALUES (%s,%s);"""
    try:
        cur = conn.cursor()
        # cur.execute("""INSERT INTO l2ig_db(line_id,wallet_id) VALUES ('test_line_id=====','======test_wallet_id');""")
        cur.execute(sql,(line_id,wallet_id,))
        conn.commit()
        cur.close()
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    select_test()
    # insert_test('1','2')
