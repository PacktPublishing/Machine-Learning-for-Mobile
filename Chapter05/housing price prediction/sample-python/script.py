import numpy as np
import pandas as pd
from coremltools.converters.sklearn import _linear_regression
from pandas.core import series
from sklearn import datasets, linear_model
import sklearn
from sklearn.metrics import mean_squared_error, r2_score
import coremltools

boston = datasets.load_boston()

bos = pd.DataFrame(boston.data)

bos.columns = boston.feature_names

bos['price'] = boston.target

x = bos.drop('price',axis=1)
y = bos.price

X_train,X_test,Y_train,Y_test = sklearn.model_selection.train_test_split(x,y,test_size=0.3,random_state=5)

lm = sklearn.linear_model.LinearRegression()

lm.fit(X_train, Y_train)

model = coremltools.converters.sklearn.convert(
    sk_obj=lm,
    input_features=boston.feature_names,
    output_feature_names='price')

model.save('HousePricer.mlmodel')