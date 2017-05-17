import numpy as np
from sklearn.naive_bayes import GaussianNB


x = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
y = np.array([1, 1, 1, 2, 2, 2])

clf = GaussianNB() # create classifer
clf.fit(x,y)
GaussianNB(priors=None)

print(clf.predict([[-0.2, -1]]))