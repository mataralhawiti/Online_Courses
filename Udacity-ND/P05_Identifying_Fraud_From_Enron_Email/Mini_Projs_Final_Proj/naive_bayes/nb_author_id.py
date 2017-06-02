#!/usr/bin/python

""" 
    This is the code to accompany the Lesson 1 (Naive Bayes) mini-project. 

    Use a Naive Bayes Classifier to identify emails by their authors
    
    authors and labels:
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




######################################################### Training
### your code goes here ###
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score


## classifier
clf = GaussianNB()


## fit the classfier on training features and lables
t0 = time()
clf.fit(features_train,labels_train)
print "training time:", round(time()-t0, 3), "s"


######################################################### 

## use the trained classifier to predict labels for the test features
t1 = time()
predict = clf.predict(features_test)
print "predicting time:", round(time()-t1, 3), "s"



### calculate and return the accuracy on the test data
accuracy = accuracy_score(predict, labels_test)

print accuracy

'''
0.973265073948
training time: 0.719 s
testing time: 0.114 s

'''

