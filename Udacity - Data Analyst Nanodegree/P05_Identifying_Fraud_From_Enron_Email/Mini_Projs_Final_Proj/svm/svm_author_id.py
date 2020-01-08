#!/usr/bin/python

""" 
    This is the code to accompany the Lesson 2 (SVM) mini-project.

    Use a SVM to identify emails from the Enron corpus by their authors:    
    Sara has label 0
    Chris has label 1
"""
    
import sys
from time import time
sys.path.append("../tools/")
from email_preprocess import preprocess
import numpy as np


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()




#########################################################
### your code goes here ###

#########################################################

from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

#clf = SVC(kernel= 'linear')

clf = SVC(kernel= 'rbf', C=10000.0)

# train 
# -- uncomment this if you want to make smaller training set
# features_train = features_train[:len(features_train)/100] 
# labels_train = labels_train[:len(labels_train)/100] 

t0 = time()
clf.fit(features_train, labels_train)
print "training time:", round(time()-t0, 3), "s"


# predict
t1 = time()

pred = clf.predict(features_test) # remeber it's a list [] !!!
#red = clf.predict(features_test[50])
print "predicting time:", round(time()-t1, 3), "s"


# accuracy

#accuracy = accuracy_score(pred, labels_test)
accuracy = accuracy_score(pred, labels_test)
print accuracy


print np.sum(pred==1) # Chris







'''
training time: 128.076 s
predicting time: 14.261 s
0.984072810011


--------------------------------------------------- C with small training set :
10 : 
training time: 0.071 s
predicting time: 0.773 s
0.616040955631


100 :
training time: 0.073 s
predicting time: 0.775 s
0.616040955631

1000 :
training time: 0.069 s
predicting time: 0.738 s
0.821387940842

10000 :
training time: 0.067 s
predicting time: 0.629 s
0.892491467577



Does this C value correspond to a simpler or more complex decision boundary?
Larger C is more accuract but more complex descion boundray
----------------------


---------- full training set, with large C :
training time: 77.477 s
predicting time: 7.817 s
0.990898748578


+++++++++++++++++++++++++++++++++++++++

Hopefully it’s becoming clearer what Sebastian meant when he said Naive Bayes is great for text--it’s faster and generally gives better performance than an SVM for this particular problem. Of course, there are plenty of other problems where an SVM might work better. Knowing which one to try when you’re tackling a problem for the first time is part of the art and science of machine learning. In addition to picking your algorithm, depending on which one you try, there are parameter tunes to worry about as well, and the possibility of overfitting (especially if you don’t have lots of training data).

Our general suggestion is to try a few different algorithms for each problem. Tuning the parameters can be a lot of work, but just sit tight for now--toward the end of the class we will introduce you to GridCV, a great sklearn tool that can find an optimal parameter tune almost automatically.


'''