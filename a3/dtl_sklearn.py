from sklearn.datasets import load_iris
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier

def SkLearn(max_depth):
    clf = DecisionTreeClassifier(criterion='entropy', max_depth=max_depth)
    clf.fit(trn_mtx, trn_labels)
    train_pred = clf.predict(trn_mtx)
    print "Accuracy: ", accuracy_score(trn_labels, train_pred) * 100