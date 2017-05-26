""" quiz materials for feature scaling clustering """

### FYI, the most straightforward implementation might 
### throw a divide-by-zero error, if the min and max
### values are the same
### but think about this for a second--that means that every
### data point has the same value for that feature!  
### why would you rescale it?  Or even use it at all?
from __future__ import division
from sklearn.preprocessing import MinMaxScaler
import numpy as np

def featureScaling(arr):
	scaled_features = []
	min_arr = min(arr)
	max_arr = max(arr)

	for i in arr:
		x = (i-min_arr) / (max_arr-min_arr) #decimal
		#x = (i-min_arr) // (max_arr-min_arr) #interger
		scaled_features.append(x)
	return scaled_features

## tests of your feature scaler--line below is input data
#data = [115, 140, 175]
#print featureScaling(data)



weights = np.array([[115.], [140.], [175.]])
scaler = MinMaxScaler()
rescaled_weight = scaler.fit_transform(weights)
print rescaled_weight