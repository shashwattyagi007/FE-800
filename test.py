import re
import pandas as pd
import numpy as np
import seaborn as snb
import matplotlib.pyplot as plt
from pdfminer.pdfinterp import PDFResourceManager , PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import io as IO
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from nltk import tokenize

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    strio = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, strio, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = strio.getvalue()

    fp.close()
    device.close()
    strio.close()
    return text


lone=convert_pdf_to_txt('/Users/shreyastro/Desktop/Desktop_files/Stevens_Statements/spring_2019/FE800/Reports/tesla.pdf')
xx = str(re.findall(r'ITEM 1A(.*?)ITEM 1B',lone,re.DOTALL))

xxy=xx.split('\\n')

shear = [re.sub("[^a-zA-Z]+", " ", s) for s in xxy]

shear = [re.sub("htm", " ", s) for s in shear]

shear = [x for x in shear if x != '']

shear = [x for x in shear if x != ' ']

shear=[i.replace('x c','') for i in shear ]

vect=CountVectorizer(ngram_range=(1,1),stop_words='english')

dtm=vect.fit_transform(shear)

pd.DataFrame(dtm.toarray(),columns=vect.get_feature_names())

lda=LatentDirichletAllocation(n_components=10)
lda_dtf = lda.fit_transform(dtm)
sorting=np.argsort(lda.components_)[:,::-1]
features=np.array(vect.get_feature_names())

import mglearn
mglearn.tools.print_topics(topics=range(10), feature_names=features,
sorting=sorting, topics_per_chunk=5, n_words=5)
