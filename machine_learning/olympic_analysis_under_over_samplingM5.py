
# Importing the necessary libraries
import warnings
warnings.simplefilter('ignore')
import pandas as pd
import numpy as np

from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder

from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold
from numpy import mean
from numpy import std

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report


# Reading the dataset
olympic_data = pd.read_csv("final_olympic_data.csv")
olympic_data.head()


# Columns available in the dataset
olympic_data_columns = olympic_data.columns.tolist()
olympic_data_columns

# Getting data Stats
data_stats = olympic_data.describe()
data_stats



# Getting the null count columnwise
column_null_counts = olympic_data.isnull().sum(axis=0)
column_null_counts


# count
olympic_data["medal"].value_counts()


olympic_data["medal"] = olympic_data["medal"].fillna(0)


olympic_data["is_medal"] = np.where(olympic_data["medal"] == 0, 0, 1)
olympic_data.head()



#Getting required columns
olympic_data = olympic_data[["sex","season","event_category","region","is_medal","age","height","weight"]]
olympic_data.head()


#Check data types
olympic_data.dtypes


# # Use Label Encoder on categorical columns


#Label Encoding
columns = ["sex", "season", "event_category", "region"]
le_sex=LabelEncoder()
le_season=LabelEncoder()
le_event=LabelEncoder()
le_region=LabelEncoder()


#Label Encoding
olympic_data["sex"]=le_sex.fit_transform(olympic_data["sex"])
olympic_data["season"]=le_season.fit_transform(olympic_data["season"])
olympic_data["event_category"]=le_event.fit_transform(olympic_data["event_category"])
olympic_data["region"]=le_region.fit_transform(olympic_data["region"])
olympic_data.head()


#Check what represents what 
print(le_sex.inverse_transform(olympic_data["sex"]))
print(le_season.inverse_transform(olympic_data["season"]))
print(le_event.inverse_transform(olympic_data["event_category"]))
print(le_region.inverse_transform(olympic_data["region"]))


# # Split the dataframe into winter and summer 
# 

#Splitting the dataframe into winter and summer
temp=olympic_data.season==0
winter_data=olympic_data[~temp]
summer_data=olympic_data[temp]



winter_data.head()


summer_data.head()


# # Train test winter and summer data

#Train Test Split Winter
X_W = winter_data.drop(["is_medal"], axis=1)
y_W = np.array(winter_data["is_medal"])

validation_size = 0.20
seed = 6
X_train_W, X_test_W, Y_train_W, Y_test_W = train_test_split(X_W,y_W,test_size = validation_size, random_state = seed)


#Train Test Split Summer
X_S = summer_data.drop(["is_medal"], axis=1)
y_S = np.array(summer_data["is_medal"])

validation_size = 0.20
seed = 6
X_train_S, X_test_S, Y_train_S, Y_test_S = train_test_split(X_S,y_S,test_size = validation_size, random_state = seed)


# # Random Forest Classifier and Decision Tree Classifier
# ### Make_pipeline, use IterativeImputer, StandardScaler on Models.

#Random Forest and Decision Tree Classifier
model_RF=RandomForestClassifier()
model_DTC=DecisionTreeClassifier()


pipeline_RF_W=make_pipeline(IterativeImputer(),
                         StandardScaler(),
                         model_RF)
pipeline_DTC_W=make_pipeline(IterativeImputer(),
                         StandardScaler(),
                         model_DTC)
pipelines_W=[("Random Forest", pipeline_RF_W),("Decision Tree",pipeline_DTC_W)]


#cross validation for Winter Data 
results_W = []
names_W = []
for name, pipeline in pipelines_W:
    kfold = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
    cv_results = cross_val_score(pipeline, X_train_W, Y_train_W, cv=kfold, scoring="accuracy")
    results_W.append(cv_results)
    names_W.append(name)
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)


# # Predictions and Classification Reports

#Predctions for winter data
predictions_W=[]
for name,pipeline in pipelines_W:
    pipeline.fit(X_train_W,Y_train_W)
    predictions_W.append(pipeline.predict(X_test_W))


#Classification report on winter data
for i in range(len(predictions_W)):
    print("{} classification report".format(pipelines_W[i][0]))
    print(classification_report(Y_test_W, predictions_W[i]))


#Random Forest and Decision Tree Classifier Summer
model_RF=RandomForestClassifier()
model_DTC=DecisionTreeClassifier()


pipeline_RF_S=make_pipeline(IterativeImputer(),
                         StandardScaler(),
                         model_RF)
pipeline_DTC_S=make_pipeline(IterativeImputer(),
                         StandardScaler(),
                         model_DTC)
pipelines_S=[("Random Forest", pipeline_RF_S),("Decision Tree",pipeline_DTC_S)]


#cross validation for Summer Data
results_S = []
names_S = []
for name, pipeline in pipelines_S:
    kfold = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
    cv_results = cross_val_score(pipeline, X_train_S, Y_train_S, cv=kfold, scoring="accuracy")
    results_S.append(cv_results)
    names_S.append(name)
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)


#Predctions for Summer data
predictions_S=[]
for name,pipeline in pipelines_S:
    pipeline.fit(X_train_S,Y_train_S)
    predictions_S.append(pipeline.predict(X_test_S))



#Classification report on Summer data
for i in range(len(predictions_S)):
    print("{} classification report".format(pipelines_S[i][0]))
    print(classification_report(Y_test_S, predictions_S[i]))


# # Class Imbalance use SMOTE and RandomUnderSampler on winter and summer data

from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline


#First impute and scale original data sets
# define imputer
imputer = IterativeImputer()
# fit on the dataset
imputer.fit(X_W)
imputer.fit(X_S)
# transform the dataset
X_W_imp = imputer.transform(X_W)
X_S_imp = imputer.transform(X_S)

validation_size = 0.20
seed = 6
X_train_W, X_test_W, Y_train_W, Y_test_W = train_test_split(X_W_imp,y_W,test_size = validation_size, random_state = seed)
X_train_S, X_test_S, Y_train_S, Y_test_S = train_test_split(X_S_imp,y_S,test_size = validation_size, random_state = seed)


#Fix the issue with class imbalance winter data
scaler=StandardScaler()
model=DecisionTreeClassifier()
over=SMOTE(sampling_strategy=0.15)
under=RandomUnderSampler(sampling_strategy=0.9)
steps=[('scale',scaler),('over',over),('under',under),('model',model)]
pipeline_W=Pipeline(steps=steps)
kfold = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
cv_results = cross_val_score(pipeline_W, X_train_W, Y_train_W, cv=kfold, scoring="accuracy")
print("Accuracy: {}({})".format(cv_results.mean(),cv_results.std()))


pipeline_W.fit(X_train_W,Y_train_W)
predictions_W=pipeline_W.predict(X_test_W)


print("Winter Data")
print(classification_report(Y_test_W,predictions_W))



#Fix the issue with class imbalance summer data
scaler=StandardScaler()
model=DecisionTreeClassifier()
over=SMOTE(sampling_strategy=0.15)
under=RandomUnderSampler(sampling_strategy=0.9)
steps=[('scale',scaler),('over',over),('under',under),('model',model)]
pipeline_S=Pipeline(steps=steps)
kfold = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
cv_results = cross_val_score(pipeline_S, X_train_S, Y_train_S, cv=kfold, scoring="accuracy")
print("Accuracy: {}({})".format(cv_results.mean(),cv_results.std()))


pipeline_S.fit(X_train_S,Y_train_S)
predictions_S=pipeline_S.predict(X_test_S)


print("Summer Data")
print(classification_report(Y_test_S,predictions_S))

