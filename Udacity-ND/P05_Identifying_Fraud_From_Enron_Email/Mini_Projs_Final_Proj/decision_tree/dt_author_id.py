#!/usr/bin/python

""" 
    This is the code to accompany the Lesson 3 (decision tree) mini-project.

    Use a Decision Tree to identify emails from the Enron corpus by author:    
    Sara has label 0
    Chris has label 1
"""
    
import sys
from time import time
sys.path.append("../tools/")
from email_preprocess import preprocess


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()




#########################################################
### your code goes here ###
#########################################################

from sklearn import tree
from sklearn.metrics import accuracy_score



# -- train
clf = tree.DecisionTreeClassifier(min_samples_split=40)
t0 = time()
clf = clf.fit(features_train, labels_train)
print "training time:", round(time()-t0, 3), "s"



# -- predict/test
t1 = time()
pred = clf.predict(features_test)
print "predicting time:", round(time()-t1, 3), "s"


# -- accuracy
accuracy = accuracy_score(pred, labels_test)

print accuracy


# number of features 
print len(features_train[0])
print len(features_test[0])


# 0.993174061433
# 40: 0.977815699659