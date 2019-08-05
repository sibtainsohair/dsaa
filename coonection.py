import pymysql

con = pymysql.connect(host="localhost", user='root',
                           passwd='admin',
                           database='DSA')

with con:
    cur = con.cursor()

