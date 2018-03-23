import MySQLdb

def connection():

    conn=MySQLdb.connect(host='localhost', user='root', password='12345',db='todo')
    cur=conn.cursor()

    return cur,conn

