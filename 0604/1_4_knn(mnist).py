# -*- coding: utf-8 -*-
"""1-4.KNN(mnist).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1noLXwPMSVr28qh7H_8vjmxBAM27OK09X
"""

# KNN으로 mnist 데이터를 학습한다.
# --------------------------------
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

# mnist 데이터를 가져온다.
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train[:5000]
y_train = y_train[:5000]
x_test = x_test[:1000]
y_test = y_test[:1000]

# x_train[0]의 이미지를 확인한다.
plt.imshow(x_train[0])
plt.show()

# shape을 변경한다. 3D --> 2D
x_train = x_train.reshape(-1, 784)
x_test = x_test.reshape(-1, 784)

x_train.shape

# 0 ~ 1 사잇값으로 표준화 한다.
x_train = x_train / 255
x_test = x_test / 255

# KNN 으로 Train 데이터 세트를 학습한다.
knn = KNeighborsClassifier(n_neighbors=5, p=2, metric='minkowski')
knn.fit(x_train, y_train)

# Test 세트의 Feature에 대한 class를 추정하고, 정확도를 계산한다
# accuracy = knn.score(testX, testY)와 동일함.
y_pred = knn.predict(x_test)
accuracy = (y_test == y_pred).mean()
print()
print("* 시험용 데이터로 측정한 정확도 = %.2f" % accuracy)

