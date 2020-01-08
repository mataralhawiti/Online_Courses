#!/usr/bin/python

""" 
    Starter code for exploring the Enron dataset (emails + finances);
    loads up the dataset (pickled dict of dicts).

    The dataset has the form:
    enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

    {features_dict} is a dictionary of features associated with that person.
    You should explore features_dict as part of the mini-project,
    but here's an example to get you started:

    enron_data["SKILLING JEFFREY K"]["bonus"] = 5600000
    
"""

import pickle

enron_data = pickle.load(open("../final_project/final_project_dataset.pkl", "r"))


# How many data points (people) are in the dataset?
print len(enron_data.keys())

# For each person, how many features are available?
print len(enron_data['METTS MARK'])



# The "poi" feature records whether the person is a person of interest, according to our definition. How many POIs are there in the dataset?
poi = 0
for key, value in enron_data.items():
	if enron_data[key]["poi"] == True :
		poi+=1

print poi


# What is the total value of the stock belonging to James Prentice?
print enron_data['PRENTICE JAMES']['total_stock_value']

# How many email messages do we have from Wesley Colwell to persons of interest?
print enron_data['COLWELL WESLEY']['from_this_person_to_poi']

# What is the value of stock options exercised by Jeffrey K Skilling?
print enron_data['SKILLING JEFFREY K']['exercised_stock_options']

#
#
#

# Of these three individuals (Lay, Skilling and Fastow), who took home the most money (largest value of "total_payments" feature)?
# How much money did that person get?

print max(enron_data['LAY KENNETH L']['total_payments'],
	enron_data['SKILLING JEFFREY K']['total_payments'],
	enron_data['FASTOW ANDREW S']['total_payments'])



# How many folks in this dataset have a quantified salary? What about a known email address?
salary = 0
for key, value in enron_data.items():
	if enron_data[key]['salary'] != 'NaN' :
		salary += 1
print salary


email_address = 0
for key, value in enron_data.items():
	if enron_data[key]['email_address'] != 'NaN' :
		email_address += 1
print email_address




"""
A python dictionary can't be read directly into an sklearn classification or regression algorithm; 
instead, it needs a numpy array or a list of lists (each element of the list (itself a list) is a data point, and the elements of the smaller list are the features of that point).

We've written some helper functions (featureFormat() and targetFeatureSplit() 
in tools/feature_format.py) that can take a list of feature names and the data dictionary, and return a numpy array.

In the case when a feature does not have a value for a particular person, this function will also replace the feature value with 0 (zero).
"""


#
#

"""

As you saw a little while ago, not every POI has an entry in the dataset (e.g. Michael Krautz). 
Thats because the dataset was created using the financial data you can find in final_project/enron61702insiderpay.pdf, 
which is missing some POIs (those absences propagated through to the final dataset). On the other hand, for many of these "missing" POIs, we do have emails.

While it would be straightforward to add these POIs and their email information to the E+F dataset, and just put "NaN" for their 
financial information, this could introduce a subtle problem. You will walk through that here.


How many people in the E+F dataset (as it currently exists) have "NaN" for their total payments? What percentage of people in the dataset as a whole is this?

"""

total_payments = 0
for key, value in enron_data.items():
	if enron_data[key]['total_payments'] == 'NaN' :
		total_payments += 1
print total_payments
print total_payments / 146 # 14%




# How many POIs in the E+F dataset have "NaN" for their total payments? What percentage of POIs as a whole is this?
poi_total_payments = 0
for key, value in enron_data.items():
	if enron_data[key]["poi"] == True and enron_data[key]['total_payments'] == 'NaN':
		poi_total_payments+=1

print poi_total_payments # 0%



# If a machine learning algorithm were to use total_payments as a feature, would you expect it to associate a "NaN" value with POIs or non-POIs?
'Yes, correct. No training points would have "NaN" for total_payments when the class label is "POI"'

