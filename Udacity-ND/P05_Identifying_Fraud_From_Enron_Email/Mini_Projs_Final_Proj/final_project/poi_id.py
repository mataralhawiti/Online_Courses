#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")
import matplotlib.pyplot
from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from sklearn.feature_selection import SelectKBest
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn import tree
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.grid_search import GridSearchCV


### Task 1: Select what features you'll use.

"""
	features_list is a list of strings, each of which is a feature name.
	The first feature must be "poi".
"""

features_list = ['poi','salary'] # You will need to use more features

# Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

# Exploring our dataset (Matar):
data_points = len(data_dict)
features = len(data_dict[data_dict.keys()[0]]) # get first key from the returned list
poi_lables = sum([ p["poi"] for p in data_dict.values() if p["poi"] == 1])

print "No. of data points : ", data_points
print "No. of features : ", features
print "No. of POI : " , poi_lables




### Task 2: Remove outliers

""" 
	follwoing [outliers] mini-project,
	Intutivly, If we have outliers I'd assume they will somewhere around financial data.
	I find "salary" and "bounse" features most compeling for outliers,
	so I'm going to plot them to see if we have outlier
"""

for point in data_dict.values():
	matplotlib.pyplot.scatter( point['salary'], point['bonus'])

matplotlib.pyplot.xlabel("salary")
matplotlib.pyplot.ylabel("bonus")
matplotlib.pyplot.show()


""" let us find this outlier"""
max_bonus = max([ i["bonus"] for i in data_dict.values() if i["bonus"] != 'NaN'])

 
for key, value in data_dict.items():
	if data_dict[key]["bonus"] == max_bonus :
		outlier_key =  key
		break


""" remove the outlier, plot again"""
data_dict.pop(outlier_key,0)

for point in data_dict.values():
	matplotlib.pyplot.scatter( point['salary'], point['bonus'])

matplotlib.pyplot.xlabel("salary")
matplotlib.pyplot.ylabel("bonus")
matplotlib.pyplot.show()





### Task 3: Create new feature(s)

# Store to my_dataset for easy export below.
my_dataset = data_dict


# Extract features and labels from dataset for local testing

""" 
	1 : I'll create new feature which I'll call earned_cash (salary+bonus)
"""

for point in my_dataset:
	p = my_dataset[point]
	if p['salary'] == 'NaN' and p['bonus'] == 'NaN' :
		p['earned_cash'] = 'NaN'
	elif p['salary'] != 'NaN' and p['bonus'] == 'NaN' :
		p['earned_cash'] = p['salary']
	elif p['salary'] == 'NaN' and p['bonus'] != 'NaN' :
		p['earned_cash'] = p['bonus']
	else :
		p['earned_cash'] = p['salary'] + p['bonus']




""" 
	2 : Now, I'll prepare features_list that I will use 
"""
features_list = features_list + ['bonus',  'earned_cash', 'total_stock_value', 'expenses','long_term_incentive','director_fees', 
									 'from_this_person_to_poi','shared_receipt_with_poi']


data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

""" 
	3 :  7 best features and prepare my final features list
"""
KBest_features = SelectKBest(k='all')
KBest_features.fit(features, labels)

my_features_list = zip(features_list[1:], KBest_features.scores_) #Zip feature with its score
my_features_list = sorted(my_features_list, key=lambda x: x[1], reverse=True)[:7] # let's sort desc based on score x[1], and pick top 7

my_features_list = [ f[0] for f in my_features_list ]
my_features_list = ['poi'] + my_features_list


""" 
	4: extract my final features from the dataset
"""
data = featureFormat(my_dataset, my_features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)



### Task 4: Try a varity of classifiers
"""
	Please name your classifier clf for easy export below.
	Note that if you want to do PCA or other multi-stage operations,
	you'll need to use Pipelines. For more info:
	http://scikit-learn.org/stable/modules/pipeline.html

	Provided to give you a starting point. Try a variety of classifiers.
"""



### Task 5: Tune your classifier to achieve better than .3 precision and recall 
"""
	using our testing script. Check the tester.py script in the final project
	folder for details on the evaluation method, especially the test_classifier
	function. Because of the small size of the dataset, the script uses
	stratified shuffle split cross validation. For more info: 
	http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

	Example starting point. Try investigating other evaluation techniques!
"""



features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)





#--------------------------------------------------------------------------------------------- NB
clf = GaussianNB()

"""
clf = GaussianNB()
clf = clf.fit(features_train, labels_train)
pred = clf.predict(features_test)

precision = precision_score(labels_test, pred)
recall 	  = recall_score(labels_test, pred)

print precision
print recall
 0.84536082  0.15463918
"""


#--------------------------------------------------------------------------------------------- DR



"""
param_grid = {'criterion': ["gini", "entropy"],
 			  'max_depth': [None, 2, 4, 6,8,10],
 			  'min_samples_split': [5, 10, 15,20,25,30,35,40,45,50]
                }

tr = tree.DecisionTreeClassifier()
clf = GridSearchCV(tr, param_grid)
clf = clf.fit(features_train, labels_train)


print clf.best_params_
#{'min_samples_split': 40, 'criterion': 'entropy', 'max_depth': None}

#clf = tree.DecisionTreeClassifier(criterion="entropy", max_depth=None, min_samples_split=50)

"""






### Task 6: Dump your classifier, dataset, and features_list so anyone can
"""
check your results. You do not need to change anything below, but make sure
that the version of poi_id.py that you submit can be run on its own and
generates the necessary .pkl files for validating your results.
"""

dump_classifier_and_data(clf, my_dataset, features_list)
