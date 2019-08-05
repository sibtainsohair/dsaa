from tokenization import *
import MySQLdb
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
import extraction

def connection():
    conn = MySQLdb.connect(host="localhost",
                           user = 'root',
                           passwd = 'myadmin',
                           database = 'DSA')
    c = conn.cursor()
    return c, conn

def insert_tweets(tweets):
    query = "INSERT INTO tweets(tweet,originalscore,reversescore,totaltweetscore) " \
            "VALUES(%s,%s,%s,%s)"

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.executemany(query, tweets)

        conn.commit()
    except Error as e:
        print('Error:', e)

    def insert_keyword(keyword):
        query = "INSERT INTO keyword(keyword,keywordtotalscore) " \
                "VALUES(%s,%s)"

        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)

            cursor = conn.cursor()
            cursor.executemany(query, keyword)

            conn.commit()
        except Error as e:
            print('Error:', e)

        finally:
            cursor.close()
            conn.close()


def main():
    keywords = [(keyword, score)]
    insert_keyword(keywords)

    tweets = [(originaltext,score,revscore,score)]
    insert_tweets(tweets)


if __name__ == '__main__':
    main()