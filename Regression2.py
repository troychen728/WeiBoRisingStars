# -*- coding: utf-8 -*-
"""
"""
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.formula.api as sm

#### read csv file
csv_file = pd.read_csv('Paneldatamodified.csv')
difflike = csv_file['difflike']
likes = csv_file['likes']
plike = difflike/likes
diffco = csv_file['diffco']
comment = csv_file['comment']
pcomment = diffco/comment
diffrepo = csv_file['diffrepo']
repost = csv_file['repost']
prepost = diffrepo/repost
difffo = csv_file['difffo']
follower = csv_file['follower']
pfollower = difffo/follower
idindex = csv_file['idindex']

''' Use the first 10 ids as training set and run regression1'''

index = idindex[idindex <=10]
y1 = pfollower[index]

X1 = np.zeros([len(y1), 3])
X1[:, 0] = prepost[index]
X1[:, 1] = pcomment[index]
X1[:, 2] = plike[index]
#
#
X_train1, X_test, y_train1, y_test = train_test_split(X1, y1, test_size=0.2)
regressor = LinearRegression()

regressor.fit(X_train1[:30, :], y_train1[:30])
plt.scatter(X_train1[:, 0], y_train1, color='red')
regressor_OLS = sm.OLS(endog = y1, exog = X1).fit()
print(regressor_OLS.summary())

index = idindex[idindex >= 30]

X2 = np.zeros([len(index), 3])
X2[:, 0] = prepost[index]
X2[:, 1] = pcomment[index]
X2[:, 2] = plike[index]
predict1=regressor.predict(X2)

'''Use the 10~20 ids as training set and run regression2'''
index = idindex[idindex >10 && idindex<=20]
y1 = pfollower[index]

X1 = np.zeros([len(y1), 3])
X1[:, 0] = prepost[index]
X1[:, 1] = pcomment[index]
X1[:, 2] = plike[index]
#
#
X_train1, X_test, y_train1, y_test = train_test_split(X1, y1, test_size=0.2)
regressor = LinearRegression()

regressor.fit(X_train1[:30, :], y_train1[:30])
plt.scatter(X_train1[:, 0], y_train1, color='red')
regressor_OLS = sm.OLS(endog = y1, exog = X1).fit()
print(regressor_OLS.summary())

index = idindex[idindex >= 30]

X2 = np.zeros([len(index), 3])
X2[:, 0] = prepost[index]
X2[:, 1] = pcomment[index]
X2[:, 2] = plike[index]
predict2=regressor.predict(X2)

'''Use the 20~30 ids as training set and run regression3'''
index = idindex[idindex >10 && idindex<=20]
y1 = pfollower[index]

X1 = np.zeros([len(y1), 3])
X1[:, 0] = prepost[index]
X1[:, 1] = pcomment[index]
X1[:, 2] = plike[index]
#
#
X_train1, X_test, y_train1, y_test = train_test_split(X1, y1, test_size=0.2)
regressor = LinearRegression()

regressor.fit(X_train1[:30, :], y_train1[:30])
plt.scatter(X_train1[:, 0], y_train1, color='red')
regressor_OLS = sm.OLS(endog = y1, exog = X1).fit()
print(regressor_OLS.summary())

index = idindex[idindex >= 30]

X2 = np.zeros([len(index), 3])
X2[:, 0] = prepost[index]
X2[:, 1] = pcomment[index]
X2[:, 2] = plike[index]
predict3=regressor.predict(X2)

##make final prediction#
pfollower = pfollower[index]
pfollower_predict = (predict1+predict2+predict3)/3
falserate = abs((pfollower_predict - pfollower)/pfollower)
falserate = np.array(falserate)
trueflag = []
for i in range(len(falserate)):
    if falserate[i] < 0.2:
        trueflag.append([1])
    else:
        trueflag.append([0])

meantrueflag = np.mean(trueflag)
print('Mean = %f' %meantrueflag)

## output 3 users with the biggest pfollower prediction**
high = np.argsort(pfollower_predict, axis = 0)[::-1]

users = high[:3]
print("3 users with biggest pfollower prediction")
print(csv_file.iloc(users.tolist()))