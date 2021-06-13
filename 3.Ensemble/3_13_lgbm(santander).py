# -*- coding: utf-8 -*-
"""3-13.LGBM(santander).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DONfeWYX-Wu8pDoMPOaBbyJRdbadjE42
"""

import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GridSearchCV

# Commented out IPython magic to ensure Python compatibility.
# %cd '/content/drive/My Drive/Colab Notebooks'

# There are no missing values in this dataset, it looks like that Santander 
# already cleaned and preprocessed the data.
df = pd.read_csv("data/santander.csv", encoding='latin-1')

df.info()
df.describe()
df['TARGET'].value_counts()
df['var3'].value_counts()

# 'var3' feature의 -999999를 2로 치환하고, 'ID' feature는 drop한다.
df['var3'].replace(-999999, 2, inplace=True)
df.drop('ID', axis = 1, inplace=True)

# 피처와 레이블 세트를 분리하고, 학습/평가/시험 데이터를 생성한다.
X_features = df.iloc[:, :-1]
y_labels = df.iloc[:, -1]

X_train, X_test, y_train, y_test = train_test_split(X_features, y_labels, test_size = 0.2, stratify=y_labels)
X_train, X_eval, y_train, y_eval = train_test_split(X_train, y_train, test_size = 0.2, stratify=y_train)

# 레이블 분포가 고른지 확인한다. 고르지 않다. accuracy로 평가하는 것보다 ROC-AUC로 평가하는 것이 적합하다.
y_train.value_counts() / len(y_train)
y_test.value_counts() / len(y_test)
y_eval.value_counts() / len(y_eval)

# 모델 생성
lgb = LGBMClassifier(n_estimators = 100, boosting="goss", top_rate=0.2, other_rate=0.1, is_unbalance = True, silent=True)

# 학습
params = {'top_rate' : [0.1, 0.2, 0.3],
          'other_rate' : [0.1, 0.2, 0.3], 
          'reg_lambda' : [0, 0.5]}

gridcv = GridSearchCV(lgb, param_grid = params, cv = 3)
gridcv.fit(X_train, y_train, early_stopping_rounds=100, eval_set=[(X_eval, y_eval)], eval_metric="auc")

print('GridSearchCV 최적 파라메터 :', gridcv.best_params_)

# 평가
pred = gridcv.predict_proba(X_test)[:, 1]
auc = roc_auc_score(y_test, pred)
print("ROC AUC = {0:.4f}".format(auc))
