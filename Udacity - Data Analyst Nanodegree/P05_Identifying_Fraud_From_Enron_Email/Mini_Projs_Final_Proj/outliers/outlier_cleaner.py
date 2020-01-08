#!/usr/bin/python

def outlierCleaner(predictions, ages, net_worths):
    """
        Clean away the 10% of points that have the largest
        residual errors (difference between the prediction
        and the actual net worth).

        Return a list of tuples named cleaned_data where 
        each tuple is of the form (age, net_worth, error).
    """
    
    """
    remeber : all numpy array [1][0]
    """
    cleaned_data = []
    error_list = []


    ### your code goes here
    for i in range(len(predictions)) :
        error = (net_worths[i][0] - predictions[i][0] ) **2
        error_list.append((ages[i][0], net_worths[i][0], error))

    error_list.sort(key=lambda t: t[2], reverse=True)
    cleaned_data = error_list[8:]


    return cleaned_data#[limit:]


"""

    cleaned_data = []

    errors = (net_worths-predictions)**2
    cleaned_data =zip(ages,net_worths,errors)
    cleaned_data = sorted(cleaned_data,key=lambda x:x[2][0], reverse=True)
    limit = int(len(net_worths)*0.1)


    return cleaned_data[limit:]
"""
