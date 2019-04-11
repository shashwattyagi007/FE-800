# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 17:48:58 2019

@author: Jean Martin Guest
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
train = data[data['Year'] < 2016]
test = data[data['Year'] >= 2016]

#mport and Define Stopwords
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.extend(['.Risk','Factors','Item','1A','1B'])

#Remove new lines
def strip_newline(series):
    return [review.replace('\n','') for review in series]

train['Text'] = strip_newline(train['1A_Text'])
test['Text'] = strip_newline(test['1A_Text'])
#train['Text'][21:22].values

#warning:
#A value is trying to be set on a copy of a slice from a DataFrame.
#Try using .loc[row_indexer,col_indexer] = value instead

#Tokenize and remove punctuation
def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))
        
words_tr = list(sent_to_words(train.Text))
words_te = list(sent_to_words(test.Text))

#words_tr[21][:10]

def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

words_tr = remove_stopwords(words_tr)
words_te = remove_stopwords(words_te)

def bigrams(words, bi_min=15, tri_min=10):
    bigram = gensim.models.Phrases(words, min_count = bi_min)
    trigram = gensim.models.Phrases(bigram[words], min_count = tri_min)
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)
    return bigram_mod, trigram_mod

bigram_tr, trigram_tr = bigrams(words_tr)

#Check some words
#print(trigram_tr[bigram_tr[words[16345]]][:200])

#Remove stopwords and lemmatize
nlp = spacy.load('en', disable=['parser', 'ner'])

def lemmatization(texts, allowed_postags=['NOUN','ADJ','VERB','ADV']):
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

#Run test through trained model
trigrams_tr = [trigram_tr[bigram_tr[review]] for review in words_tr]
lemma_lg = lemmatization(trigrams_tr)
with open('lemma_lg.pkl', 'wb') as f:
    pickle.dump(lemma_lg, f)
    







#HDP model from Gensim
id2word_lg = gensim.corpora.Dictionary(lemma_lg)
id2word_lg.filter_extremes(no_below=10, no_above=0.35)
id2word_lg.compactify()
id2word_lg.save('train_dict_lg')
corpus_lg = [id2word_lg.doc2bow(text) for text in lemma_lg]

with open('corpus_lg.pkl', 'wb') as f:
    pickle.dump(corpus_lg, f)

hdp = HdpModel(corpus_lg, id2word_lg, chunksize=1000000)

len(hdp.print_topics())


#LDA model

def get_corpus(df):
    """
    Get Bigram Model, Corpus, id2word mapping
    """
    
    df['text'] = strip_newline(df.text)
    words = list(sent_to_words(df.text))
    words = remove_stopwords(words)
    bigram = bigrams(words)
    bigram = [bigram[review] for review in words]
#     lemma = lemmatization(bigram)
    id2word = gensim.corpora.Dictionary(bigram)
    id2word.filter_extremes(no_below=10, no_above=0.35)
    id2word.compactify()
    corpus = [id2word.doc2bow(text) for text in bigram]
    return corpus, id2word, bigram

train_corpus4, train_id2word4, bigram_train4 = get_corpus(train)


#len(words_te)



