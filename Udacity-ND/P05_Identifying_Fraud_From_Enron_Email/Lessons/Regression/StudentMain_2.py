#!/usr/bin/python

import numpy
import matplotlib
matplotlib.use('agg')

import matplotlib.pyplot as plt
from studentRegression import studentReg
from class_vis import prettyPicture, output_image

from ages_net_worths import ageNetWorthData

ages_train, ages_test, net_worths_train, net_worths_test = ageNetWorthData()



reg = studentReg(ages_train, net_worths_train)


print "kate networth prediction :", reg.predict([27])
print "slop" , reg.coef_
print "intercept ", reg.intercept_


print "r-squared score : ", reg.score(ages_test, net_worths_test)

print "r-squared score : ", reg.score(ages_train, net_worths_train)
