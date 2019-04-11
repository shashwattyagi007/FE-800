#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 19:27:38 2019

@author: shreyastro
"""


#LDA as an input to a classifier script:
#Reference links (delete later):
#Tutorial:https://towardsdatascience.com/unsupervised-nlp-topic-models-as-a-supervised-learning-input-cf8ee9e5cf28
#Github w/ code: https://github.com/marcmuon/nlp_yelp_review_unsupervised/tree/master/notebooks
#To avoid getting lost in the sauce:
#https://radimrehurek.com/gensim/models/ldamodel.html

#import basic libraries
import pandas as pd
import os

#import ML libraries
import pickle
import gensim
import pyLDAvis
import pyLDAvis.gensim
import spacy
import nltk; nltk.download('stopwords')
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
import re
import warnings
from pprint import pprint
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB, MultinomialNB
import mord
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from mord import LAD
import seaborn as sns
from sklearn.metrics import f1_score
from sklearn import linear_model
from sklearn import metrics
from sklearn.model_selection import KFold
from sklearn.metrics import fbeta_score
import matplotlib.pyplot as plt

import sklearn

#set new wd based on wherever file is located
os.chdir(r'/Users/shreyastro/Desktop/Desktop_files/Stevens_Statements/spring_2019/FE800')

#load in Pandas dataframe
data =pd.read_csv('final_dataframe.csv', encoding = "cp1252") #this is encoding for Windows

#Check data types
print(data.dtypes)

#Split into training and testing sets
rev_train = data[data['Year'] < 2016]
rev_test = data[data['Year'] >= 2016]

#mport and Define Stopwords
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.extend(['.Risk','Factors','Item','1A','1B'])

#Remove new lines
def strip_newline(series):
    return [review.replace('\n','') for review in series]


nlp = spacy.load('en', disable=['parser', 'ner'])

def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))
        
def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]



def bigrams(words, bi_min=15, tri_min=10):
    bigram = gensim.models.Phrases(words, min_count = bi_min)
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    return bigram_mod



def get_corpus(df):
    """
    Get Bigram Model, Corpus, id2word mapping
    """
    
    df['Text'] = strip_newline(df['1A_Text'])
    words = list(sent_to_words(df['Text']))
    words = remove_stopwords(words)
    bigram = bigrams(words)
    bigram = [bigram[review] for review in words]
#     lemma = lemmatization(bigram)
    id2word = gensim.corpora.Dictionary(bigram)
    id2word.filter_extremes(no_below=10, no_above=0.35)
    id2word.compactify()
    corpus = [id2word.doc2bow(text) for text in bigram]
    return corpus, id2word, bigram


train_corpus4, train_id2word4, bigram_train4 = get_corpus(rev_train)

with open('train_corpus4.pkl', 'wb') as f:
    pickle.dump(train_corpus4, f)
with open('train_id2word4.pkl', 'wb') as f:
      pickle.dump(train_id2word4, f)
with open('bigram_train4.pkl', 'wb') as f:
      pickle.dump(bigram_train4, f)


with open('train_corpus4.pkl', 'rb') as f:
    train_corpus4 = pickle.load(f)
with open('train_id2word4.pkl', 'rb') as f:
    train_id2word4 = pickle.load(f)
with open('bigram_train4.pkl', 'rb') as f:
    bigram_train4 = pickle.load(f)
    
    
import logging
logging.basicConfig(filename='lda_model.log', format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    lda_train4 = gensim.models.ldamulticore.LdaMulticore(
                           corpus=train_corpus4,
                           num_topics=20,
                           id2word=train_id2word4,
                           chunksize=100,
                           workers=7, # Num. Processing Cores - 1
                           passes=50,
                           eval_every = 1,
                           per_word_topics=True)
    lda_train4.save('lda_train4.model')


lda_train4.print_topics(20,num_words=15)[:10]


train_vecs = []
for i in range(len(rev_train)):
    top_topics = lda_train4.get_document_topics(train_corpus4[i], minimum_probability=0.0)
    topic_vec = [top_topics[i][1] for i in range(20)]
    topic_vec.extend([len(rev_train.iloc[i].Text)]) # length review
    train_vecs.append(topic_vec)
    
train_vecs

X = np.array(train_vecs)
y = np.array(rev_train.Risk)
with open('y.pkl', 'wb') as f:
    pickle.dump(y, f)
with open('X.pkl', 'wb') as f:
    pickle.dump(X, f)



kf = KFold(5, shuffle=True, random_state=42)
cv_lr_f1, cv_lrsgd_f1, cv_svcsgd_f1,  = [], [], []

for train_ind, val_ind in kf.split(X, y):
    # Assign CV IDX
    X_train, y_train = X[train_ind], y[train_ind]
    X_val, y_val = X[val_ind], y[val_ind]
    
    # Scale Data
    scaler = StandardScaler()
    X_train_scale = scaler.fit_transform(X_train)
    X_val_scale = scaler.transform(X_val)

    # Logisitic Regression
    lr = LogisticRegression(
        class_weight= 'balanced',
        solver='newton-cg',
        fit_intercept=True
    ).fit(X_train_scale, y_train)

    y_pred = lr.predict(X_val_scale)
    cv_lr_f1.append(f1_score(y_val, y_pred, average='binary'))
    
    # Logistic Regression Mini-Batch SGD
    sgd = linear_model.SGDClassifier(
        max_iter=1000,
        tol=1e-3,
        loss='log',
        class_weight='balanced'
    ).fit(X_train_scale, y_train)
    
    y_pred = sgd.predict(X_val_scale)
    cv_lrsgd_f1.append(f1_score(y_val, y_pred, average='binary'))
    
    # SGD Modified Huber
    sgd_huber = linear_model.SGDClassifier(
        max_iter=1000,
        tol=1e-3,
        alpha=20,
        loss='modified_huber',
        class_weight='balanced'
    ).fit(X_train_scale, y_train)
    
    y_pred = sgd_huber.predict(X_val_scale)
    cv_svcsgd_f1.append(f1_score(y_val, y_pred, average='binary'))

print(f'Logistic Regression Val f1: {np.mean(cv_lr_f1):.3f} +- {np.std(cv_lr_f1):.3f}')
print(f'Logisitic Regression SGD Val f1: {np.mean(cv_lrsgd_f1):.3f} +- {np.std(cv_lrsgd_f1):.3f}')
print(f'SVM Huber Val f1: {np.mean(cv_svcsgd_f1):.3f} +- {np.std(cv_svcsgd_f1):.3f}')

def get_bigram(df):
    """
    For the test data we only need the bigram data built on 2017 reviews,
    as we'll use the 2016 id2word mappings. This is a requirement due to 
    the shapes Gensim functions expect in the test-vector transformation below.
    With both these in hand, we can make the test corpus.
    """
    df['Text'] = strip_newline(df['1A_Text'])
    words = list(sent_to_words(df['Text']))
    words = remove_stopwords(words)
    bigram = bigrams(words)
    bigram = [bigram[review] for review in words]
#     lemma = lemmatization(bigram)
    return bigram



bigram_test = get_bigram(rev_test)

with open('train_id2word4.pkl', 'rb') as f:
    train_id2word = pickle.load(f)

with open('bigram_test.pkl', 'wb') as f:
    pickle.dump(bigram_test, f)
    
with open('bigram_test.pkl', 'rb') as f:
    bigram_test = pickle.load(f)
    
lda_train4 = gensim.models.ldamulticore.LdaMulticore.load('lda_train4.model')

test_corpus = [train_id2word.doc2bow(text) for text in bigram_test]


test_vecs = []
for i in range(len(rev_test)):
    top_topics = lda_train4.get_document_topics(test_corpus[i], minimum_probability=0.0)
    topic_vec = [top_topics[i][1] for i in range(20)]
    topic_vec.extend([len(rev_test.iloc[i].Text)]) # length review
    test_vecs.append(topic_vec)
    
len(test_vecs)


import numpy as np
X = np.array(test_vecs)
y = np.array(rev_test.Risk)

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score


ss = StandardScaler()
X = ss.fit_transform(X)

lr = LogisticRegression(
  class_weight= 'balanced',
  solver='newton-cg',
  fit_intercept=True
  ).fit(X, y)

y_pred_lr = lr.predict(X)
print(f1_score(y, y_pred_lr,average='binary'))

sgd_huber = linear_model.SGDClassifier(
        max_iter=1000,
        tol=1e-3,
        alpha=20,
        loss='modified_huber',
        class_weight='balanced',shuffle=True
    ).fit(X, y)
    
y_pred_huber = sgd_huber.predict(X)
print(f1_score(y, y_pred_huber, average='binary'))
