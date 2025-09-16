from pymongo.mongo_client import MongoClient
import pandas as pd
import json

#uri
uri="mongodb+srv://<email>_db_user:<password>@cluster0.c477iiq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

#new client and connect
client=MongoClient(uri)

DATABASE_NAME="FaultDetect" 
COLLECTION_NAME="waferfault"

df=pd.read_csv("../notebooks/wafer_data.csv")

df=df.drop(columns=["Unnamed: 0"],axis=1)

json_record = list(json.loads(df.T.to_json()).values())

#uplad_json data mongodb
client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)