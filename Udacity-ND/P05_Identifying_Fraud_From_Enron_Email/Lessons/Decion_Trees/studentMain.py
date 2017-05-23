#!/usr/bin/python

""" lecture and example code for decision tree unit """

import sys
from class_vis import prettyPicture, output_image
from prep_terrain_data import makeTerrainData

import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
from classifyDT import classify, classify_min_samples_split_2, classify_min_samples_split_50

features_train, labels_train, features_test, labels_test = makeTerrainData()



### the classify() function in classifyDT is where the magic
### happens--fill in this function in the file 'classifyDT.py'!
#clf = classify(features_train, labels_train)
#pred = clf.predict(features_test)


# min_samples_split
clf2 = classify_min_samples_split_2(features_train, labels_train)
clf50 = classify_min_samples_split_50(features_train, labels_train)


pred2 = clf2.predict(features_test)
pred50 = clf50.predict(features_test)

from sklearn.metrics import accuracy_score


# accuracy (no parameter)
#acc = accuracy_score(pred, labels_test)

acc2 = accuracy_score(pred2, labels_test)
acc50 = accuracy_score(pred50, labels_test)


print round(acc2,3)
print round(acc50,3)





#### grader code, do not modify below this line

# prettyPicture(clf, features_test, labels_test)
# output_image("test.png", "png", open("test.png", "rb").read())
