from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import os
import json
from utils import load_json,read_csv
from sklearn.preprocessing import MinMaxScaler



def read_data(community_key,data_path,institute_path):
    data=load_json(data_path)
    institutes=load_json(institute_path)
    
    X=[]
    y=[]
    
    for i in range(len(institutes)):
        institute=institutes[i]
        rank=i
        score=institute["score"]
        faculty=institute["faculty"]
        sample=[]
        flag=0
        for key in community_key:
            if key in data[institute["name"]].keys():
                flag+=data[institute["name"]][key]
                sample.append(data[institute["name"]][key])
            else:
                sample.append(0.0)
        #sample=list(data[institute["name"]].values())
        #sample.append(score) # normalize to 0 and 1
        sample.append(faculty)
        #print(sample)
        if flag>1:
            #print(sample)
            X.append(sample)
            y.append(score)

    return X,y



data_path="./cleaned_data/inst_comm.json"
institute_path="./cleaned_data/institut_ranking.json"
community_path="./cleaned_data/community.csv"
reader=read_csv(community_path)

community_key=['oth']

for line in reader[1:]:
    line=line[0]
    id,com_id,method,problem=line.split("; ")[0],line.split("; ")[1],line.split("; ")[2],line.split("; ")[3]
    if problem!='other':
        community_key.append(com_id)

community_key=list(set(community_key))
#print(len(set(community_key)))

X,y=read_data(community_key,data_path,institute_path)


# Create an instance of the MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))

print(len(X))
print(len(y))

print(max(y))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

#print(X_train[0])



model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)


# Calculate R-squared

r_squared = model.score(X_train, y_train)

print("R-squared:", r_squared)

r_squared = model.score(X_test, y_test)

print("R-squared:", r_squared)

coefficients = model.coef_
intercept = model.intercept_

print("Coefficients:", coefficients)
print("Intercept:", intercept)

# Step 7: Evaluate the model
#mse = mean_squared_error(y_test, y_pred)

#print(mse)