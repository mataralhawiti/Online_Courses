#!/usr/bin/python


"""
    Starter code for the evaluation mini-project.
    Start by copying your trained/tested POI identifier from
    that which you built in the validation mini-project.

    This is the second step toward building your POI identifier!

    Start by loading/formatting the data...
"""

import pickle
import sys
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit

data_dict = pickle.load(open("../final_project/final_project_dataset.pkl", "r") )

### add more features to features_list!
features_list = ["poi", "salary"]

data = featureFormat(data_dict, features_list)
labels, features = targetFeatureSplit(data)



### your code goes here 
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn import cross_validation


features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(features, labels,test_size=0.3,random_state=42)

clf = tree.DecisionTreeClassifier()
clf = clf.fit(features_train, labels_train)

acc = clf.score(features_test, labels_test)

print acc

# How many POIs are predicted for the test set for your POI identifier? ### remeber : it's not asking about TRUE, it's asking about predicated
pred = clf.predict(features_test) #1.0
print int(sum(pred))

# How many people total are in your test set?
print len(features_test)

# If your identifier predicted 0. (not POI) for everyone in the test set, what would its accuracy be?
print 1.0 - (4.0/29) # 4.0 : predicted correctly ... 


"""
As you may now see, having imbalanced classes like we have in the Enron dataset (many more non-POIs than POIs) 
introduces some special challenges, namely that you can just guess the more common 
class label for every point, not a very insightful strategy, and still get pretty good accuracy!

Precision and recall can help illuminate your performance better. 
Use the precision_score and recall_score available in sklearn.metrics to compute those quantities.
"""

from sklearn.metrics import *

# What's the precision?
print precision_score(labels_test, pred)

# What's the recall? 
print recall_score(labels_test, pred)



"""
In the final project you'll work on optimizing your POI identifier, 
using many of the tools learned in this course. Hopefully one 
result will be that your precision and/or recall will go up, 
but then you'll have to be able to interpret them. 

Here are some made-up predictions and true labels for a 
hypothetical test set; fill in the following boxes to practice identifying true positives, 
false positives, true negatives, and false negatives. Lets use the convention that "1" signifies a positive result, and "0" a negative. 
"""

predictions = [0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1] 
true_labels = [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0]

# how many true positive ? (1:1)
6

# What's the precision of this classifier?
print precision_score(true_labels, predictions)

# What's the recall of this classifier?
print recall_score(true_labels, predictions)