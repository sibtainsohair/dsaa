from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import bigrams
import string
import re
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
import tweepy as tw
import csv
import codecs
from coonection import *
import sys
import time

def mypro(userinput):
    start = time.time()

    PERIOD_OF_TIME = 20



    consumer_key = 'nE1gXsExmmiqLMHOkzSbcOhtk'
    consumer_secret = 'JJG2nFpX1lW6PX6ctavyFrbnFKtKIAqELDtmH19lNCpFkJpIYo'
    access_token = '190197768-2eYByJYUErl79UghFULOjtIX2TssfxHtikT1mpBf'
    access_token_secret = 'TtJIQdgHK439r4pHRdHOgNbGWGYL6uHTI97FO6T1cOeyq'


    emoticons_str = r"""
        (?:
            [:=;] # Eyes
            [oO\-]? # Nose (optional)
            [D\)\]\(\]/\\OpP] # Mouth
        )"""

    regex_str = [
        emoticons_str,
        r'<[^>]+>',  # HTML tags
        r'(?:@[\w_]+)',  # @-mentions
        r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
        r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs

        r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
        r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
        r'(?:[\w_]+)',  # other words
        r'(?:\S)'  # anything else
    ]

    tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
    emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)


    def tokenize(s):
        return tokens_re.findall(s)


    def preprocess(s, lowercase=False):
        tokens = tokenize(s)
        if lowercase:
            tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
        return tokens

    punctuation = list(string.punctuation)
    #stop = stopwords.words('english') + punctuation + ["b'", 'via', 'â', '', '¦']
    stop = punctuation + ["b'", 'via', 'â', '', '¦', 's']

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    # Open/Create a file to append data
    print("Enter Keyword: ")
    hashtag = userinput
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
        return


    file_name = hashtag + '.csv'
    csvFile = open(file_name, 'a', newline='')
    # Use csv Writer
    csvWriter = csv.writer(csvFile)
    sql_insert_query = " INSERT INTO `keywords` (`keyword_name`) VALUES (%s)"
    insert_tuple = (hashtag)
    cur.execute(sql_insert_query, insert_tuple)
    con.commit()
    sql_insert_query = " SELECT k_id from keywords where keyword_name LIKE %s"
    insert_tuple = (hashtag)
    cur.execute(sql_insert_query, insert_tuple)
    result = cur.fetchone()
    keyword_id = result[0]



    for tweet in tw.Cursor(api.search, q=hashtag + '-filter:retweets', lang="en", tweet_mode="extended", compression=False,).items(200):
        print(tweet.full_text.encode('utf-8'))
        csvWriter.writerow([tweet.full_text.encode('utf-8')])
        #i = i+1
    csvFile.close()


    with open('nb_traindata.csv', 'rb') as f:
        reader = csv.reader(codecs.iterdecode(f, 'utf-8'))
        train_list = list((map(tuple, reader)))

    '''''''''''train = [
        ('I love this sandwich.', 'pos'),
        ('This is an amazing place!', 'pos'),
        ('I feel very good about these beers.', 'pos'),
        ('This is my best work.', 'pos'),
        ("What an awesome view", 'pos'),
        ('I do not like this restaurant', 'neg'),
        ('I am tired of this stuff.', 'neg'),
        ("I can't deal with this", 'neg'),
        ('He is my sworn enemy!', 'neg'),
        ('My boss is horrible.', 'neg')
    ]'''''''''''

    cl = NaiveBayesClassifier(train_list)
    #f.close()

    pos = 0
    neg = 0
    #csvfileread = open('pr.csv', 'r', newline='')
    with open(file_name, 'rb') as f:
        reader = csv.reader(codecs.iterdecode(f, 'utf-8'))
        my_list = list((map(tuple, reader)))
    #csvupdatefile = csv.reader(csvfileread)
    row_count = len(my_list)
    print(row_count)
    #csvblaafile = csv.writer(csvwritefile, lineterminator='\n')
    originaltext = ''
    for i in range(len(my_list)):
        row=my_list[i]
        row = str(row)
        for word in preprocess(row):
            if word not in stop and not word.startswith(('#', '@', 'http', 'nhttp', 'x', "b'")) and (word != ('b' or "b'")):
                #print(word)
                wordstr = str(word)
                originaltext += wordstr + ' '
        print(originaltext)
        blob = TextBlob(originaltext,classifier=cl)
        #label = blob.classify()
        #print(label)
        #print(originaltext)
        #prob_dist = cl.prob_classify(originaltext)
        #scores = round(prob_dist.prob(label), 2)
        score = blob.sentiment.polarity
        if(score>0):
            revscore=(score*-1)+0.1
            pos+=1
        elif(score==0):
            revscore=score
        else:
            revscore=(score*-1)-0.1
            neg+=1
        print(score)
        print(revscore)
        sql_insert_query = " INSERT INTO `tweets`(`k_id`,`original_score`, `reversed_score`) VALUES (%s,%s,%s)"
        insert_tuple = (keyword_id, score, revscore)
        cur.execute(sql_insert_query, insert_tuple)
        con.commit()
        originaltext=''
        #if time.time() > start + PERIOD_OF_TIME:
         #   break
    #csvfileread.close()
    pos_percent = (pos/row_count)*100
    neg_percent = (neg/row_count)*100
    neu_percent = 100 - (pos_percent + neg_percent)
    if(pos>neg):
        label = 'positive'
        sql_insert_query = " UPDATE `keywords` SET `sentiment_lable` = %s,`pos_percentage` = %s, `neg_percentage` = %s, `neu_percentage` = %s WHERE `k_id` = %s"
        insert_tuple = (label, pos_percent, neg_percent,neu_percent, keyword_id)
        cur.execute(sql_insert_query, insert_tuple)
        con.commit()
        print('overall result: ' + label)
        print('positive tweets: ')
        print(pos_percent)
        print("negative tweets: ")
        print(neg_percent)
        print("neutral tweets: ")
        print(neu_percent)
    else:
        label = 'negative'
        sql_insert_query = " UPDATE `keywords` SET `sentiment_lable` = %s,`pos_percentage` = %s, `neg_percentage` = %s WHERE `k_id` = %s"
        insert_tuple = (label, pos_percent, neg_percent, keyword_id)
        cur.execute(sql_insert_query, insert_tuple)
        con.commit()
        print('overall result: ' + label)
        print('positive tweets: ')
        print(pos_percent)
        print("negative tweets: ")
        print(neg_percent)
        print("neutral tweets: ")
        print(neu_percent)







            #print(cl.classify(originaltext))
            #print(cl.accuracy(originaltext))
        #for val in originaltext:
             #   csvwritefile.writelines(originaltext)
            #csvwritefile.writelines('\n')
            #originaltext = ''



    #csvwritefile.close()'''''
    #con.commit()


