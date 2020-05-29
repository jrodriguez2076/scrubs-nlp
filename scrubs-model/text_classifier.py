# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 12:35:06 2020

@author: Jose
"""

import numpy as np
import re
import pickle
import nltk
from nltk.corpus import stopwords
from sklearn.datasets import load_files
nltk.download('stopwords')


# importing dataset
reviews  = load_files('txt_sentoken/')
X,y = reviews.data, reviews.target


#storing as picke files
with open('X.pickle', 'wb') as f:
    pickle.dump(X, f)
    
with open('y.pickle', 'wb') as f:
    pickle.dump(y, f)
    
# unpicking
# with open('X.pickle', 'rb') as f:
#    Xo = pickle.load(f)

    
# CREATE CORPUS
corpus = []
for i in range (0,len(X)):
    review = re.sub(r'\W', ' ',str(X[i]))
    review = review.lower()
    review = re.sub(r'\s+[a-z]\s+', ' ', review)
    review = re.sub(r'^[a-z]\s+', ' ', review)
    review = re.sub(r'\s+', ' ', review)
    corpus.append(review)


# CREATE A BAG OF WORDS MODEL
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(max_features=2000,min_df=3, max_df=0.6, stop_words= stopwords.words('english'))
X = vectorizer.fit_transform(corpus).toarray()


# CREATE TF-IDF FROM BOW MODEL
from sklearn.feature_extraction.text import TfidfTransformer
transformer = TfidfTransformer()
X = transformer.fit_transform(X).toarray()

# ALTERNATIVE - CREATE A TF_IDF MODEL DIRECTLY FROM CORPUS
from sklearn.feature_extraction.text import TfidfVectorizer
tfVectorizer = TfidfVectorizer(max_features=2000,min_df=3, max_df=0.6, stop_words= stopwords.words('english'))
X = tfVectorizer.fit_transform(corpus).toarray()


#SPLIT DATASET INTO TRAINING AND TEST
from sklearn.model_selection import train_test_split
text_train, text_test, sent_train, sent_test = train_test_split(X, y, test_size = 0.2, random_state=0)


#GET REGRESSION MODEL
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression()
classifier.fit(text_train, sent_train)


# TEST MODEL PERFORMANCE
sent_pred = classifier.predict(text_test)
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(sent_test, sent_pred)


# SAVING MODEL FOR LATER USE
with open('model.pickle', 'wb') as f:
    pickle.dump(classifier, f)
 
    
# SAVING VECTORIZER
with open('vectorizer.pickle','wb') as f:
    pickle.dump(tfVectorizer,f)
