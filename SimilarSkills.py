
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[8]:


# Reading in and setting up the adjacency matrix
Adj=pd.read_csv('https://datajam2018.blob.core.windows.net/eventopendata/ne_data/dwp_data/adzuna_adjacency_201709_201808.csv')
Adj=Adj.set_index('skills')


# In[10]:


# Calculating correlation matrix
Diag=Adj.max()
B=Adj.divide(Diag)
Corr=B.multiply(B.transpose())


# In[20]:


# Choosing n skills most correlated to user's skills (mySkills)
def SimilarSkills(mySkills, n) :
    m=len(mySkills)
    Similar=Corr.loc[mySkills].sum()
    Similar=Similar.sort_values(ascending=False)[m:]
    return Similar[:n]

mySkills = ['.Net', 'Sales','Marketing','Business Development']
SimilarSkills(mySkills, 10)

