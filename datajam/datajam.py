from flask import Flask, render_template, url_for, request, redirect
from flask_bootstrap import Bootstrap 

from sklearn import preprocessing, neighbors, svm
from sklearn.model_selection import train_test_split, GridSearchCV
import numpy as np
import pandas as pd
import csv
from flask_bootstrap import Bootstrap 

from flask import jsonify
import json
import requests

import csv
import locale
locale.setlocale(locale.LC_ALL, 'en_GB.UTF-8')

app = Flask(__name__)
Bootstrap(app)

#Adj=''
Adj = pd.read_csv('adzuna_adjacency_201709_201808.csv')
Adj = Adj.set_index('skills')
Diag = Adj.max()
B = Adj.divide(Diag)
Corr = B.multiply(B.transpose())

#SkillSalary=''
SkillSalary = pd.read_csv('adzuna_skill_salary_median.csv', index_col=0)
Salary = SkillSalary.loc[201807]


SkillJobs=pd.read_csv('adzuna_skills_jobs_201704_201803.csv')
SkillJobs=SkillJobs.set_index('normalised_job_title')

JobFreq=SkillJobs.sum(axis=0) # Get total frequency for all skills
RelativeFreq=SkillJobs.div(JobFreq, axis=1) # For each skill get raltive frequency of jobs

# In[116]:


# For a list of skills return related job titles



@app.route('/')
def home():

    return render_template('index.html')

@app.route('/djresult', methods=['POST'])
def form():
    global Adj
    global SkillSalary

    print(request.form)
    skill = request.form.getlist('skills[]')
    pretty_skill = ', '.join(skill)

    fo = SkillSalary[skill].loc[201807]
    string_value1 = str(fo)
    yup = locale.currency(fo.mean(), grouping=True)
    salary = yup.decode("utf8")
	
    with open('adzuna_skill_salary_median.csv', 'rt') as f:
         reader = csv.reader(f, delimiter=',') # good point by @paco
         for row in reader:
            for field in row:
              if field == skill:
                datajam_pred = field

    def SimilarSkills(mySkills, n):
        m = len(mySkills)
        Similar = Corr.loc[mySkills].sum()
        Similar = Similar.sort_values(ascending=False)[m:]
        return Similar[:n].index.values

    def SimilarSalary(mySkills, n):
        mySimilarSkills = SimilarSkills(mySkills, 10)
        mySimilarSalary = Salary[mySimilarSkills]
        return mySimilarSalary

    def RelatedJobs(mySkills, n):
        MyRelativeFreq = RelativeFreq[mySkills]  # Pick out relative frequency of users skills
        myJobs = MyRelativeFreq.sum(axis=1)
        myJobs = myJobs.sort_values(ascending=False).index.values
        return myJobs[:n]

    def CurrentJobs(mySkills, n):
        mySkills_np = np.array(mySkills)
        return RelatedJobs(mySkills_np, n)

    def RecommendedJobs(mySkills, n, m):
        mySkills_np = np.array(mySkills)
        allSkills = np.append(mySkills_np, SimilarSkills(mySkills, n))
        return RelatedJobs(allSkills, m)

    other_skills = ', '.join(SimilarSkills(skill, 5))

    current_jobs = ', '.join(CurrentJobs(skill, 5))

    recommended_jobs = ', '.join(RecommendedJobs(skill, 5, 5))

    return render_template('result.html',
                           data_obj = pretty_skill,
                           data_obj2 = salary,
                           data_obj3 = other_skills,
                           data_obj4 = current_jobs,
                           data_obj5 = recommended_jobs)


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(debug=True)


