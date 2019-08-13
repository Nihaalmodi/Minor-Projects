
#--------------------------------------------Import required files-------------------------------------------------#
import pandas as pd
import numpy as np
import random

from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import f1_score,precision_score,recall_score,confusion_matrix
from matplotlib import pyplot as plt
from sklearn.tree import DecisionTreeClassifier
#---------------------------------------------for printing decision tree--------------------------------------#
try:
	import pydot
	from sklearn.tree import export_graphviz
	from sklearn.externals.six import StringIO 
except:
	pass
import warnings
warnings.filterwarnings('ignore')

from math import log1p,exp

#--------------------------------------------Load dataset-------------------------------------------------#

print("Loading Dataset")
data=pd.read_csv('kddcup.data_10_percent_corrected')
data.columns=["duration","protocol_type","service","flag","src_bytes","dst_bytes","land","wrong_fragment","urgent","hot","num_failed_logins","logged_in","num_compromised","root_shell","su_attempted","num_root","num_file_creations","num_shells","num_access_files","num_outbound_cmds","is_host_login","is_guest_login","count","srv_count","serror_rate","srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate","diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate","dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate","attack_type"]
print("Dataset Loaded")

#-----------------------------------------Check For Missing Values----------------------------------------#

print("Finding Missing Values")
if(data.isnull().values.any()):
    data.dropna(inplace=True)
print("Missing Values Deleted")

#---------------------------------------------------------------------------------#

def get_scores(dtc,X_train, Y_train, Y_predict):
    scores=cross_val_score(dtc, X_train, Y_train, cv=5)
    print "Cross Validation Score ",
    print(scores)
    print "Average Cross Validation Score",
    print(scores.mean())

    print "F score ",
    print(f1_score(Y_train, Y_predict,average='macro'))

    print "Recall Score ",
    print(recall_score(Y_train, Y_predict,average='macro'))

    print "Precision Score ",
    print(precision_score(Y_train, Y_predict, average='macro'))

    print(confusion_matrix(Y_train, Y_predict))

#---------------------------------------------------------------------------------#

def modify_weights(w,X_train, Y_train, Y_predict):   
    terror = np.zeros(len(Y_train))
    terror = np.where(abs(Y_train-Y_predict)>0.01,1,0)
    error = sum(w*terror)/sum(w)
    stage = log1p((1-error)/error)
    w = np.multiply(w,np.exp(stage*terror))
    X_train = X_train.apply(lambda x: x * w)
    return X_train,error

#---------------------------------------------------------------------------------#

def savetree(dtc):
    import os
    os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
    dot_data = StringIO() 
    export_graphviz(dtc, out_file=dot_data) 
    graph = pydot.graph_from_dot_data(dot_data.getvalue()) 
    graph[0].write_png("file.png")

#---------------------------------------------------------------------------------#

def DecisionTree(X_train,Y_train):
    dtc = DecisionTreeClassifier(max_depth=3)
    dt=dtc.fit(X_train,Y_train)
    Y_predict=dtc.predict(X_train)
    return dtc,Y_predict

#---------------------------------------------------------------------------------#

def NaiveBayes(X_train,Y_train):
    clf =MultinomialNB()
    clf.fit(X_train,Y_train)
    Y_predict=clf.predict(X_train)
    return clf, Y_predict

#-----------------------------------------Decision Tree------------------------------------------------------------#

X_train=data.drop(["protocol_type","service","flag","attack_type"],axis=1)
Y_train = data["attack_type"]
Y_train.replace(Y_train.unique(),list(range(1,len(Y_train.unique())+1)),inplace=True)
w = np.ones(len(Y_train))
while True:
    dtc, Y_predict = DecisionTree(X_train,Y_train)
    X_train, error = modify_weights(w,X_train,Y_train,Y_predict)
    print(error)
    if(error<0.5):
        get_scores(dtc,X_train,Y_train, Y_predict)
        break

#----------------------------------Navie Bayes------------------------------------------------------------#

X_train=data.drop(["protocol_type","service","flag","attack_type"],axis=1)
Y_train = data["attack_type"]
Y_train.replace(Y_train.unique(),list(range(1,len(Y_train.unique())+1)),inplace=True)
w = np.ones(len(Y_train))
while True:
    clf, Y_predict = NaiveBayes(X_train,Y_train)
    X_train, error = modify_weights(w,X_train,Y_train,Y_predict)
    print "Error",
    print(error)
    if(error<0.5):
        get_scores(clf,X_train,Y_train, Y_predict)
        break

#------------------------------------------Decison Tree + Navie's Bayes--------------------------------------------#

X_train=data.drop(["protocol_type","service","flag","attack_type"],axis=1)
Y_train = data["attack_type"]
Y_train.replace(Y_train.unique(),list(range(1,len(Y_train.unique())+1)),inplace=True)
w = np.ones(len(Y_train))
while True:
    dtc, Y_predict = DecisionTree(X_train,Y_train)
    X_train, error = modify_weights(w,X_train,Y_train,Y_predict)
    print "Error",
    print(error)
    if(error<0.5):
        break
while True:
    clf, Y_predict = NaiveBayes(X_train,Y_train)
    X_train, error = modify_weights(w,X_train,Y_train,Y_predict)
    print "Error",
    print(error)
    if(error<0.5):
        get_scores(clf,X_train,Y_train, Y_predict)
        break