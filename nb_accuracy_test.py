import csv
import textblob
import string
import codecs
import pickle
import pandas as pd
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
from textblob.sentiments import NaiveBayesAnalyzer
from textblob import Blobber

with open('nb_traindata.csv', 'rb') as f:
    reader = csv.reader(codecs.iterdecode(f, 'utf-8'))
    my_list = list((map(tuple, reader)))

with open('nb_test_data.csv', 'rb') as f:
    reader = csv.reader(codecs.iterdecode(f, 'utf-8'))
    test_list = list((map(tuple, reader)))

cl=NaiveBayesClassifier(my_list)
print("Naive Bayes accuracy:")
print(cl.accuracy(test_list)*100)

#classifier_f = open("naivebayes.pickle", "rb")
#classifiers = pickle.load(classifier_f)
#classifier_f.close()
#cl = NaiveBayesClassifier(classifiers)
#classifiers.accuracy(my_list)
#object = cl
#save_classifier = open("naivebayes.pickle","ab")
#pickle.dump(cl, save_classifier)
#save_classifier.close()

tb = Blobber(analyzer=NaiveBayesAnalyzer())

