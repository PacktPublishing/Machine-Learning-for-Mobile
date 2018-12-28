//importing required packages / modules.
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import sklearn.datasets as ds
import sklearn
import coremltools


//Loading breast cancer dataset
dataset = ds.load_breast_cancer()

//creating a pandas dataframe with data
cancerdata = pd.DataFrame(dataset.data)

//getting all the column names.
cancerdata.columns = dataset.feature_names


//Deleting all other data except the below mentioned columns to make the dataset consistent
for i in range(0,len(dataset.feature_names)):
    if ['mean concave points', 'mean area', 'mean radius', 'mean perimeter', 'mean concavity'].\
            __contains__(dataset.feature_names[i]):
        continue
    else:
        cancerdata = cancerdata.drop(dataset.feature_names[i], axis=1)


# print(cancerdata)
//Exporting the resulted data into excel
cancerdata.to_csv("myfile.csv")

//assigning types array to cancer_types
cancer_types = dataset.target_names

cancer_names = []

//getting all the corresponding cancer types with name [string] format.
for i in range(len(dataset.target)):
    cancer_names.append(cancer_types[dataset.target[i]])

# print(cancer_names)

//spliting as test & train data
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(cancerdata,cancer_names,test_size=0.3,
                                                                         random_state=5)

//Initilizing thge classifier
classifier = RandomForestClassifier()
//feeding the training data and fitting it.
classifier.fit(x_train, y_train)

//converting the fitted model to a coremlmodel file
model = coremltools.converters.sklearn.convert(classifier, input_features=list(cancerdata.columns.values), output_feature_names='typeofcancer')
model.save("cancermodel.mlmodel")

//testing the model with test data
print(classifier.predict(x_test))
cancerdata['type'] = cancer_names
cancerdata.to_csv("myfile2.csv")
# print(dataset.feature_names)