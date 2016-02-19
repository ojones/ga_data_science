import sqlite3
conn = sqlite3.connect('/Users/oj/Documents/twitter_db/sentiment.db')
cur = conn.cursor()

def procesed_text(cur, limit):
    rows = cur.execute("""
        select processedUrl_UserName_HashTag from second_run limit {limit};
        """.format(limit=limit))
    for row in rows:
        yield row[0]

def sentiment_value(cur, limit):
    rows = cur.execute("""
        select score from second_run limit {limit};
        """.format(limit=limit))
    for row in rows:
        yield row[0]

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', MultinomialNB()),
])

row_count = 50000
data = list(procesed_text(cur, row_count))
target = list(sentiment_value(cur, row_count))
text_clf = text_clf.fit(data, target)

print(len([x for x in target if x == '0']))

docs_new = ['God is love', 'OpenGL on the GPU is fast', 'i hate this', 'this is good', 'this was terrible']
predicted = text_clf.predict(docs_new)

for tweet, sentiment in zip(docs_new, predicted):
    print('%r => %s' % (tweet, sentiment))

import pickle
with open('web_classifier.p', 'wb') as f:
    pickle.dump(text_clf, f, protocol=2)