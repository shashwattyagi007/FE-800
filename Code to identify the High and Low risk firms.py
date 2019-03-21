#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import seaborn as snb


# In[2]:


z_score = pd.read_csv('final Z-score.csv')
z_score


# In[3]:


df = pd.DataFrame()
firms=z_score.columns.drop('YEAR')
firms

result = {}

for i in range(len(z_score)):
    LR = []
    HR = []
    for each in firms:
        if z_score[each][i] > 2.4:
            LR.append(each)
        else:
            if z_score[each][i]  == 0:
                pass
            else:
                HR.append(each)
    df =  df.append(pd.DataFrame([[z_score['YEAR'][i],LR,HR]],columns = ['YEAR','Low Risk','High Risk'])).reset_index(drop=True)
df_ = df.T
df_.columns = df['YEAR']
df = df_[1:]
df.T


# In[4]:


df


# In[ ]:




