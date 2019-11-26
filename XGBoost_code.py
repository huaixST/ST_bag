from turtledemo.penrose import dart
import matplotlib.pyplot  as plt
import numpy as np
import pandas as pd
import sklearn
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBClassifier
from sklearn import metrics
from sklearn.model_selection import GridSearchCV

#data reading
my_matrix = pd.read_csv("PanasPositive_Pre.csv")
data_colu_y = my_matrix['Y']
data_colu_user = my_matrix['Unnamed: 0']
data_pre = my_matrix.drop(columns=['Unnamed: 0', 'Y', 'Pre_Score'])
#data normorlization
scaler = MinMaxScaler()
scaler.fit(data_pre)
scaler.data_max_
data_normorlize = scaler.transform(data_pre)
data_new = pd.DataFrame(data_normorlize)
data_now = pd.concat([data_new, data_colu_y], axis=1)

X_train = data_new[:]
Y_train = data_colu_y[:]
Accuracy_score = []

k_range = (0,20,1)
k_scores = [0]
#a list to store three parameters
parameter = []
#triple loop to get the best model parameter
for i in np.arange(0,7,1):
    for j in np.arange(0,7,1):
        for k in k_range:
            #XGBoost training model
            clf = XGBClassifier(learning_rate=0.2,tree_method = 'exact',max_depth= i\
                                ,min_child_weight = j, n_estimators= k)
            X_train = data_new[:]
            Y_train = data_colu_y[:]
            #cross validation you could change'accuracy' into 'roc_auc' 'precision' 'recall' 'f1_macro'
            scores = cross_val_score(clf, X_train, Y_train, cv=5, scoring= 'accuracy')
            #the average of scores
            score_mean = np.mean(scores)
            k_scores.append(score_mean)
            if score_mean >  max(k_scores[:-1]):
                #i, j, k represent three parameters
                parameter.append((i, j, k))
            #print(scores)
            #print(k_scores)


            print(max(k_scores))
print(parameter)
#use plt to draw the changes of the scores
plt.plot(k_scores)
plt.xlabel()
plt.ylabel()
plt.show()

