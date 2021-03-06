# Purpose of regression, essentially to find m and b in y = mx + b (oversimplified)
# Use regression to map best-fit line (curve) to your data

import quandl, math
import numpy as np
import pandas as pd
from sklearn import preprocessing, cross_validation, svm  # Note preprocessing for scaling, feature scalars between 0, 1
from sklearn.linear_model import LinearRegression

df = quandl.get('WIKI/GOOGL')

df = df[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume', ]]  # Grab label and (potential) features
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Close']) / df['Adj. Close'] * 100.0  # Define important custom vars
df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0

df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']]  # Update data frame to match y = mx...+b format

forecast_col = 'Adj. Close'  # Use this to define forecasting column, can reuse general format for different apps
df.fillna(-99999, inplace=True)  # Fill any NA values with an outlier value

forecast_out = int(math.ceil(0.01*len(df)))  # project 10% out from the data frame

df['label'] = df[forecast_col].shift(-forecast_out)  # Shifts out for projection
df.dropna(inplace=True)  # Drops any NA (outlier) values

X = np.array(df.drop(['label'], 1))
y = np.array(df['label'])
X = preprocessing.scale(X)  # Need to scale new values alongside all others values for corr preprocessing
y = np.array(df['label'])

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

clf = LinearRegression(n_jobs=1)  # Support vector regression...can easily switch algorithms, back to LinearRegression
clf.fit(X_train, y_train)

accuracy = clf.score(X_test, y_test)  # squared error = accuracy

print(accuracy)

# NOTE: Be sure to check documentation for all algorithms when building
# Keep in mind speed - slower computers will have more and more difficulty with more complex algorithms
# Placeholder for additional notes