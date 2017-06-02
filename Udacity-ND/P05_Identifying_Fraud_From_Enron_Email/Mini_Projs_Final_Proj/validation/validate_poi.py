#!/usr/bin/python


"""
    Starter code for the validation mini-project.
    The first step toward building your POI identifier!

    Start by loading/formatting the data

    After that, it's not our code anymore--it's yours!
"""

import pickle
import sys
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit

data_dict = pickle.load(open("../final_project/final_project_dataset.pkl", "r") )

### first element is our labels, any added elements are predictor
### features. Keep this the same for the mini-project, but you'll
### have a different feature list when you do the final project.
features_list = ["poi", "salary"]

data = featureFormat(data_dict, features_list)
labels, features = targetFeatureSplit(data)



### it's all yours from here forward!  
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn import cross_validation


# clf = tree.DecisionTreeClassifier()
# clf = clf.fit(features, labels)

# acc = clf.score(features, labels)

# print acc


"""
Now you'll add in training and testing, so that you get a trustworthy accuracy number. 
Use the train_test_split validation available in sklearn.cross_validation; hold out 30% of the data for 
testing and set the random_state parameter to 42 (random_state controls which points go into the training 
set and which are used for testing; setting it to 42 means we know exactly which events are in which set, 
and can check the results you get). What's your updated accuracy?
"""

features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(features, labels,test_size=0.3,random_state=42)

clf = tree.DecisionTreeClassifier()
clf = clf.fit(features_train, labels_train)

acc = clf.score(features_test, labels_test)

print acc


