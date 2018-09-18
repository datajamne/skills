
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


# In[45]:


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


# In[51]:


# For each recommended skill return median salary
def SimilarSalary (mySkills, n) :
    mySimilarSkills=SimilarSkills(mySkills, 10)
    mySimilarSalary=Salary[mySimilarSkills.index.values]
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


# In[82]:


# For a list of skills return related job titles
JobFreq=SkillJobs.sum(axis=1) # Get total frequency for all jobs
RelativeFreq=SkillJobs.div(JobFreq, axis=0) # For each job get relative frequency of skills

def RelatedJobs (mySkills, n) :
    MyRelativeFreq=RelativeFreq[mySkills] # Pick out relative frequency of users skills
    myJobs=MyRelativeFreq.sum(axis=1)
    myJobs=myJobs.sort_values(ascending=False)
    return myJobs[:n]


# In[93]:


#mySkills = ['Sales','Marketing','Business Development','Project Management']
#mySkills =['Analysis', 'Statistics','Data','Microsoft Excel', 'R']
#Sims=SimilarSkills(mySkills,10).index.values
#AllSkills=np.append(np.array(mySkills),Sims)
#RelatedJobs(mySkills.append(SimilarSkills(mySkills,10)),10)
#RelatedJobs(AllSkills,10)

