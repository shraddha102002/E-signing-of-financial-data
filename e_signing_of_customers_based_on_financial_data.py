# -*- coding: utf-8 -*-
"""E signing of customers based on financial data.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rjv0isNML2MbJB7-Rf8j3hH-UWazMyeg

# Part 1: Data preprocessing

## Importing the libraries and dataset
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dataset = pd.read_csv('/content/financial_data.csv')

"""## Data exploration"""

dataset.head()

dataset.shape

dataset.columns

dataset.info()

# statistical summary
dataset.describe()

"""## Dealing with the null values"""

dataset.isnull().values.any()

dataset.isnull().values.sum()

"""## Encoding the categorical data"""

dataset.select_dtypes(include='object').columns

len(dataset.select_dtypes(include='object').columns)

dataset['pay_schedule'].unique()

dataset['pay_schedule'].nunique()

dataset.shape

dataset = pd.get_dummies(data=dataset, drop_first=True)

dataset.head()

dataset.shape

len(dataset.select_dtypes(include='object').columns)

"""## Countplot"""

sns.countplot(dataset['e_signed'])

# e-signed values
(dataset.e_signed == 1).sum()

# not e-signed values
(dataset.e_signed == 0).sum()

"""## Restructure the dataset"""

dataset.head()

dataset['months employeed'] = (dataset.months_employed + dataset.years_employed *12)

dataset.head()

dataset = dataset.drop(columns=['months_employed', 'years_employed'])

dataset.head()

dataset['personnal account months'] = (dataset.personal_account_m + dataset.personal_account_y *12)

dataset.head()

dataset = dataset.drop(columns=['personal_account_m', 'personal_account_y'])

dataset.head()

"""## Correlation matrix and heatmap"""

dataset_2 = dataset.drop(columns=['entry_id', 'e_signed'])

dataset_2.corrwith(dataset['e_signed']).plot.bar(
    figsize=(16, 9), title = 'Correlated with e_signed', grid=True
)

# heatmap
plt.figure(figsize=(16,9))
ax = sns.heatmap(dataset.corr(), annot=True)

"""## Splitting the dataset"""

dataset.head()

# independent variables / matrix features
x = dataset.drop(columns=['entry_id', 'e_signed'])

# target variable
y = dataset['e_signed']

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

x_train.shape

y_train.shape

x_test.shape

y_test.shape

"""## Feature scaling"""

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()

x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

x_train

x_test

"""# Part 2: Building the model

## 1) Logistic regression
"""

from sklearn.linear_model import LogisticRegression
classifier_lr = LogisticRegression(random_state=0)
classifier_lr.fit(x_train, y_train)

y_pred = classifier_lr.predict(x_test)

from sklearn.metrics import confusion_matrix, accuracy_score

accuracy_score(y_test, y_pred)

confusion_matrix(y_test, y_pred)

"""## 2) SVM"""

from sklearn.svm import SVC
classifier_svc = SVC(random_state=0)
classifier_svc.fit(x_train, y_train)

y_pred = classifier_svc.predict(x_test)

from sklearn.metrics import confusion_matrix, accuracy_score
accuracy_score(y_test, y_pred)

confusion_matrix(y_test, y_pred)

"""## 3) Random forest"""

from sklearn.ensemble import RandomForestClassifier
classifier_rf = RandomForestClassifier(random_state=0)
classifier_rf.fit(x_train, y_train)

y_pred = classifier_rf.predict(x_test)

from sklearn.metrics import confusion_matrix, accuracy_score
accuracy_score(y_test, y_pred)

confusion_matrix(y_test, y_pred)

"""## 4) XGBoost Classifier"""

from xgboost import XGBClassifier
classifier_xgb = XGBClassifier(random_state=0)
classifier_xgb.fit(x_train, y_train)

y_pred = classifier_xgb.predict(x_test)

from sklearn.metrics import confusion_matrix, accuracy_score
accuracy_score(y_test, y_pred)

confusion_matrix(y_test, y_pred)

"""# Part 3: Applying Randomized Search to find the best parameters"""

from sklearn.model_selection import RandomizedSearchCV

parameters = {
    'learning_rate':[0.05, 0.10, 0.15, 0.20, 0.25, 0.30],
    'max_depth':[3, 4, 5, 6, 8, 10, 12, 15],
    'min_child_weight':[1, 3, 5, 7],
    'gamma':[0.00, 0.1, 0.2, 0.3, 0.4],
    'colsample_bytree':[0.3, 0.4, 0.5, 0.7],
    'n_estimators':[100, 200, 500],
    'subsample':[0.5, 0.7, 1.0]
}

parameters

random_cv = RandomizedSearchCV(estimator=classifier_xgb, param_distributions=parameters, n_iter=5,
                               scoring='roc_auc', n_jobs=-1, cv=5, verbose=3)

random_cv.fit(x_train, y_train)

random_cv.best_estimator_

random_cv.best_params_

random_cv.best_score_

"""# Part 4: Final model (XGBoost Classifier)"""

from xgboost import XGBClassifier
classifier = XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
              colsample_bynode=1, colsample_bytree=0.7, gamma=0.2,
              learning_rate=0.05, max_delta_step=0, max_depth=5,
              min_child_weight=1, missing=None, n_estimators=500, n_jobs=1,
              nthread=None, objective='binary:logistic', random_state=0,
              reg_alpha=0, reg_lambda=1, scale_pos_weight=1, seed=None,
              silent=None, subsample=1.0, verbosity=1)
classifier.fit(x_train, y_train)

y_pred = classifier.predict(x_test)

from sklearn.metrics import confusion_matrix, accuracy_score
accuracy_score(y_test, y_pred)

confusion_matrix(y_test, y_pred)

"""# Part 5: Predicting a single observation"""

dataset.head()

single_obs = [[45, 1, 2500,	3,	1,	600,	37000,	0.7373, 0.9035, 0.4877, 0.515977, 0.580918, 0.380918, 10, 0, 0, 0, 36, 30]]

classifier.predict(sc.transform(single_obs))