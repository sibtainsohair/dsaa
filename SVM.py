from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import random
from sklearn.metrics import accuracy_score

data = []
data_labels = []
with open("pos_tweets.txt") as f:
    for i in f:
        data.append(i)
        data_labels.append('pos')

with open("neg_tweets.txt") as f:
    for i in f:
        data.append(i)
        data_labels.append('neg')

vectorizer = CountVectorizer(
    analyzer = 'word',
    lowercase = False,
)
features = vectorizer.fit_transform(
    data
)

features_nd = features.toarray() # for easy usage

X_train, X_test, y_train, y_test  = train_test_split(
        features_nd,
        data_labels,
        train_size=0.80,
        random_state=1234)

log_model = LogisticRegression()
log_model = log_model.fit(X=X_train, y=y_train)
y_pred = log_model.predict(X_test)

j = random.randint(0,len(X_test)-7)
#for i in range(j,j+7):
    #print(y_pred[0])
    #ind = features_nd.tolist().index(X_test[i].tolist())

print("accuracy of SVM:")
print(accuracy_score(y_test, y_pred)*100)