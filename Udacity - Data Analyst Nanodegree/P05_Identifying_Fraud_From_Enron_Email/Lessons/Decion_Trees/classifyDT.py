from sklearn import tree

def classify(features_train, labels_train):
    
    ### your code goes here--should return a trained decision tree classifer
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(features_train, labels_train)
    return clf

def classify_min_samples_split_2(features_train, labels_train):
    
    ### your code goes here--should return a trained decision tree classifer
    clf = tree.DecisionTreeClassifier(min_samples_split=2)
    clf = clf.fit(features_train, labels_train)
    return clf


def classify_min_samples_split_50(features_train, labels_train):
    
    ### your code goes here--should return a trained decision tree classifer
    clf = tree.DecisionTreeClassifier(min_samples_split=50)
    clf = clf.fit(features_train, labels_train)
    return clf
  