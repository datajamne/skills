
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# *Skills Recommendation*: For a set of skills provided by user, return n skills which are the most similar

# In[8]:


# Reading in and setting up the adjacency matrix
Adj=pd.read_csv('https://datajam2018.blob.core.windows.net/eventopendata/ne_data/dwp_data/adzuna_adjacency_201709_201808.csv')
Adj=Adj.set_index('skills')


# In[10]:


# Calculating correlation matrix
Diag=Adj.max()
B=Adj.divide(Diag)
Corr=B.multiply(B.transpose())


# In[22]:


# Choosing n skills most correlated to user's skills (mySkills)
def SimilarSkills(mySkills, n) :
    m=len(mySkills)
    Similar=Corr.loc[mySkills].sum()
    Similar=Similar.sort_values(ascending=False)[m:]
    return Similar[:n]
# Test
#mySkills = ['.Net', 'Sales','Marketing','Business Development']
#SimilarSkills(mySkills, 10)


# *Salary Information*: For each recommended skill return median salary from July 2018

# In[34]:


# Get Salary information for skills, use latest reliable data
SkillSalary=pd.read_csv('https://datajam2018.blob.core.windows.net/eventopendata/ne_data/dwp_data/adzuna_skill_salary_median.csv', index_col=0)
Salary=SkillSalary.loc[201807]


# In[44]:


# For each recommended skill return median salary
def SimilarSalary (mySkills, n) :
    mySimilarSkills=SimilarSkills(mySkills, 10)
    mySimilarSalary=Salary[mySimilarSkills.index.values]
    return mySimilarSalary

# Test
#mySkills = ['Sales','Marketing','Business Development','Project Management']
#SimilarSalary(mySkills,10)

