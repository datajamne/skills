
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


# In[98]:


# Choosing n skills most correlated to user's skills (mySkills)
def SimilarSkills(mySkills, n) :
    m=len(mySkills)
    Similar=Corr.loc[mySkills].sum()
    Similar=Similar.sort_values(ascending=False)[m:]
    Similar=Similar.index.values
    return Similar[:n]
# Test
#mySkills = ['.Net', 'Sales','Marketing','Business Development']
#SimilarSkills(mySkills, 10)


# *Salary Information*: For each recommended skill return median salary from July 2018

# In[34]:


# Get Salary information for skills, use latest reliable data
SkillSalary=pd.read_csv('https://datajam2018.blob.core.windows.net/eventopendata/ne_data/dwp_data/adzuna_skill_salary_median.csv', index_col=0)
Salary=SkillSalary.loc[201807]


# In[99]:


# For each recommended skill return median salary
def SimilarSalary (mySkills, n) :
    mySimilarSkills=SimilarSkills(mySkills, 10)
    mySimilarSalary=Salary[mySimilarSkills]
    return mySimilarSalary

# Test
#mySkills = ['Sales','Marketing','Business Development','Project Management']
#mySkills =['Analysis', 'Statistics','Data','Microsoft Excel', 'R']
#SimilarSalary(mySkills,10)


# *Job Titles*: Using users current and recommended skills return related jobtitles

# In[54]:


# Get the skills and job titles data
SkillJobs=pd.read_csv('https://datajam2018.blob.core.windows.net/eventopendata/ne_data/dwp_data/adzuna_skills_jobs_201704_201803.csv')
SkillJobs=SkillJobs.set_index('normalised_job_title')


# In[116]:


# For a list of skills return related job titles
JobFreq=SkillJobs.sum(axis=0) # Get total frequency for all skills
RelativeFreq=SkillJobs.div(JobFreq, axis=1) # For each skill get raltive frequency of jobs

def RelatedJobs (mySkills, n) :
    MyRelativeFreq=RelativeFreq[mySkills] # Pick out relative frequency of users skills
    myJobs=MyRelativeFreq.sum(axis=1)
    myJobs=myJobs.sort_values(ascending=False).index.values
    return myJobs[:n]

def CurrentJobs (mySkills,n) :
    mySkills_np=np.array(mySkills)
    return RelatedJobs(mySkills_np,n)

def RecommendedJobs (mySkills, n, m) :
    mySkills_np=np.array(mySkills)
    allSkills=np.append(mySkills_np,SimilarSkills(mySkills,n))
    return RelatedJobs(allSkills,m)


# In[117]:


mySkills = ['Sales','Marketing','Business Development','Project Management']
#mySkills =['Analysis', 'Statistics','Data','Microsoft Excel', 'R']
#Sims=SimilarSkills(mySkills,10)
#AllSkills=np.append(np.array(mySkills),Sims)
#RelatedJobs(mySkills.append(SimilarSkills(mySkills,10)),10)
print(Sims)
print(CurrentJobs(mySkills,10))
print(RecommendedJobs(mySkills,10,10))

