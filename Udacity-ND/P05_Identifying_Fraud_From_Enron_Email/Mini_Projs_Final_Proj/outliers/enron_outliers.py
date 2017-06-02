#!/usr/bin/python

import pickle
import sys
import matplotlib.pyplot
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit


### read in data dictionary, convert to numpy array
data_dict = pickle.load( open("../final_project/final_project_dataset.pkl", "r") )


# 1
# What's the name of the dictionary key of this data point? (e.g. if this is Ken Lay, the answer would be "LAY KENNETH L").
#max(d, key=lambda x: d[x]['count'])
max_bonus = max([ i["bonus"] for i in data_dict.values() if i["bonus"] != 'NaN'])
print max_bonus

for key, value in data_dict.items():
	if data_dict[key]["bonus"] == max_bonus :
		print key
		break


# 2 : remove the outlier
"""
A quick way to remove a key-value pair from a dictionary is the following line: dictionary.pop( key, 0 ) 
Write a line like this (you'll have to modify the dictionary and key names, of course) and remove the outlier 
before calling featureFormat(). Now rerun the code, so your scatterplot doesnt have this outlier anymore. Are all the outliers gone?
"""

data_dict.pop("TOTAL",0)



# --- call featureFormating before calling featureFormat(). Now rerun the code, so your scatterplot doesnt have this outlier anymore. Are all the outliers gone?

features = ["salary", "bonus"]
data = featureFormat(data_dict, features)

#print max(data[1])

### your code below
for point in data:
    salary = point[0]
    bonus = point[1]
    matplotlib.pyplot.scatter( salary, bonus )

matplotlib.pyplot.xlabel("salary")
matplotlib.pyplot.ylabel("bonus")
matplotlib.pyplot.show()


# 3
"""
We would argue that theres 4 more outliers to investigate; 
lets look at a couple of them. Two people made bonuses of at least 5 million dollars, 
and a salary of over 1 million dollars; in other words, they made out like bandits. What are the names associated with those points?
"""
for key, value in data_dict.items():
	if (data_dict[key]["salary"] != 'NaN' and data_dict[key]["bonus"] != 'NaN') and (data_dict[key]["salary"] >= 1000000 and data_dict[key]["bonus"] > 5000000 ):
		print key, value
		print
