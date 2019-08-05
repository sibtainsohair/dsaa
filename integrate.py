import time

from flask import Flask, request, render_template
import tokenization
from coonection import *
app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('input.html')

@app.route('/', methods=['POST'])
def my_form_post():
    hashtag = request.form['userinput']
    tokenization.mypro(hashtag)
    sql_insert_query = "SELECT sentiment_lable,pos_percentage,neg_percentage,neu_percentage FROM keywords WHERE keyword_name LIKE %s"
    insert_tuple = (hashtag)
    cur.execute(sql_insert_query, insert_tuple)
    result = cur.fetchone()
    if cur.rowcount:
        print('overall result: ' + result[0])
        print('positive tweets: ')
        print(result[1])
        print("negative tweets: ")
        print(result[2])
        print("neutral tweets: ")
        print(result[3])
    return render_template('output.html', hash=hashtag, res=result[0], pos= result[1], neg= result[2], neu= result[3])

if __name__ == "__main__":
    app.debug = True
    app.run()