import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split as ttl
import difflib


def model():
    lb=LabelEncoder()
    rmc=RandomForestClassifier(n_estimators= 20, criterion="entropy")
    df=pd.read_csv("crop.csv")
    df1=pd.read_csv("crop.csv")
    df.insert(0, 'Sno', range(0, 0 + len(df)))
    df1.insert(0, 'Sno', range(0, 0 + len(df1)))

    y=df["Sno"]
    df["label"]=lb.fit_transform(df["label"])
    x=df.iloc[:,1:]
    x2=df[["label"]]
    x2.insert(0, 'Sno', range(0, 0 + len(x2)))
    index=[]
    for i in range(len(df)):
        item=df1[df1['Sno']==i]["label"].values[0]
        inde=x2[x2["Sno"]==i]["label"].values[0]
        index.append([item,inde])


    rmc.fit(x,y)
    return (rmc,index,df1)

def predict(result,rmc,index):
    df=pd.read_csv("crop.csv")
    df.insert(0, 'Sno', range(0, 0 + len(df)))
    r=rmc.predict([result])
    k=df[df["Sno"]==r[0]]
    for i in index:
        if(i[1]==r[0]):
            k["label"]=i[0]
            break
    return(k.values[0])
