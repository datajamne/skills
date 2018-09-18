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

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def home():

	return render_template('djhome.html')

@app.route('/djresult', methods=['POST'])
def form():
	dataframe = pd.read_csv('adzuna_skill_salary_median.csv')
	
	username = '.Net'

	fo = dataframe[username]
	string_value1 = str(fo)
	yup = fo.mean()
	
	with open('adzuna_skill_salary_median.csv', 'rt') as f:
	     reader = csv.reader(f, delimiter=',') # good point by @paco
	     for row in reader:
	        for field in row:
	          if field == username:
	            datajam_pred = field

	return render_template('djresult.html', data_obj =  datajam_pred, data_obj2 = yup)


if __name__ == '__main__':
	#app.run(debug=True)
	app.run(debug=True)


