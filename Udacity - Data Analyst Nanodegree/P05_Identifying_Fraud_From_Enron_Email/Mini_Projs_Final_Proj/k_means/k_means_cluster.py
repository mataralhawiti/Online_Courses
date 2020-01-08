#!/usr/bin/python 

""" 
    Skeleton code for k-means clustering mini-project.
"""




import pickle
import numpy
import matplotlib.pyplot as plt
import sys
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit




def Draw(pred, features, poi, mark_poi=False, name="image.png", f1_name="feature 1", f2_name="feature 2"):
    """ some plotting code designed to help you visualize your clusters """

    ### plot each cluster with a different color--add more colors for
    ### drawing more than five clusters
    colors = ["b", "c", "k", "m", "g"]
    for ii, pp in enumerate(pred):
        plt.scatter(features[ii][0], features[ii][1], color = colors[pred[ii]])

    ### if you like, place red stars over points that are POIs (just for funsies)
    if mark_poi:
        for ii, pp in enumerate(pred):
            if poi[ii]:
                plt.scatter(features[ii][0], features[ii][1], color="r", marker="*")
    plt.xlabel(f1_name)
    plt.ylabel(f2_name)
    plt.savefig(name)
    plt.show()



### load in the dict of dicts containing all the data on each person in the dataset
data_dict = pickle.load( open("../final_project/final_project_dataset.pkl", "r") )
### there's an outlier--remove it! 
data_dict.pop("TOTAL", 0)


### the input features we want to use 
### can be any key in the person-level dictionary (salary, director_fees, etc.) 
feature_1 = "salary"
feature_2 = "exercised_stock_options"
feature_3 = "total_payments"
poi  = "poi"
features_list = [poi, feature_1, feature_2, feature_3]
data = featureFormat(data_dict, features_list )
poi, finance_features = targetFeatureSplit( data )








### in the "clustering with 3 features" part of the mini-project,
### you'll want to change this line to 
### for f1, f2, _ in finance_features:
### (as it's currently written, the line below assumes 2 features)
for f1, f2, _ in finance_features:
    plt.scatter( f1, f2)
plt.show()

### cluster here; create predictions of the cluster labels
### for the data and store them to a list called pred
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=2, random_state=0)
kmeans = kmeans.fit(finance_features)
pred = kmeans.labels_ #pred = kmeans.predict(data, features_list)





### rename the "name" parameter when you change the number of features
### so that the figure gets saved to a different file
try:
    Draw(pred, finance_features, poi, mark_poi=False, name="clusters_f3.pdf", f1_name=feature_1, f2_name=feature_2)
except NameError:
    print "no predictions object named pred found, no clusters to plot"



# What are the maximum and minimum values taken by the "exercised_stock_options" feature used in this example?
max_exercised_stock_options = max(i["exercised_stock_options"] for i in data_dict.values() if i["exercised_stock_options"] != "NaN")
min_exercised_stock_options = min(i["exercised_stock_options"] for i in data_dict.values() if i["exercised_stock_options"] != "NaN")

print max_exercised_stock_options
print min_exercised_stock_options


# What are the maximum and minimum values taken by "salary"?
max_salary = max(i["salary"] for i in data_dict.values() if i["salary"] != "NaN")
min_salary = min(i["salary"] for i in data_dict.values() if i["salary"] != "NaN")

print max_salary
print min_salary




## feature scaling :
"""
Apply feature scaling to your k-means clustering code from the last lesson, on the "salary" and "exercised_stock_options" features 
(use only these two features). What would be the rescaled value of a "salary" feature that had an original value of $200,000, 
and an "exercised_stock_options" feature of $1 million? (Be sure to represent these numbers as floats, not integers!)
"""
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()



salary_np = numpy.array([[float(min_salary)],[200000.],[float(max_salary)]])
stock_np  = numpy.array([[float(min_exercised_stock_options)],[1000000.],[float(max_exercised_stock_options)]])

print scaler.fit_transform(salary_np)
print scaler.fit_transform(stock_np)