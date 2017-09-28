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
    print 'db_select'
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )

    sql = """SELECT * from l2ig_db;"""
    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            print ' ', row
        cur.close()
        return rows
    finally:
        if conn is not None:
            conn.close()


def select_by_line(line_id):
    print 'db_select by line_id'
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )

    sql = """SELECT wallet_id FROM l2ig_db WHERE line_id=%s"""
    try:
        cur = conn.cursor()
        cur.execute(sql,(line_id,))
        rows = cur.fetchall()
        cur.close()
        print rows
        return rows

    finally:
        if conn is not None:
            conn.close()

def register_new_line(line_id, wallet_id, is_auto=False):
    print 'db_insert'
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )

    sql = """INSERT INTO l2ig_db(line_id,wallet_id, is_auto) VALUES (%s,%s,%r);"""
    try:
        cur = conn.cursor()
        cur.execute(sql,(line_id,wallet_id,is_auto))
        conn.commit()
        cur.close()
    finally:
        if conn is not None:
            conn.close()

def delete_by_line(line_id):
    print 'db_delete'
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )

    sql = """DELETE FROM l2ig_db WHERE line_id=%s;"""
    try:
        cur = conn.cursor()
        cur.execute(sql,(line_id,))
        conn.commit()
        cur.close()
    finally:
        if conn is not None:
            conn.close()

def update_wallet(line_id, new_wallet_id):
    print 'db_update'
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    sql = """UPDATE l2ig_db SET wallet_id = %s WHERE line_id=%s;"""
    try:
        cur = conn.cursor()
        cur.execute(sql,(new_wallet_id,line_id))
        conn.commit()
        cur.close()
    finally:
        if conn is not None:
            conn.close()


def update_auto_state(line_id, is_auto):
    print 'db_update'
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    sql = """UPDATE l2ig_db SET is_auto = %r WHERE line_id=%s;"""
    try:
        cur = conn.cursor()
        cur.execute(sql,(is_auto,line_id))
        conn.commit()
        cur.close()
    finally:
        if conn is not None:
            conn.close()



if __name__ == '__main__':
    select_test()
    # insert_test('kakline1','kakwall2')
    # select_by_line('kakline1')
    # delete_by_line('kakline1')
