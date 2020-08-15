#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import pymongo


# In[2]:


# read cleaned data csv file from transform stage into dataframe
steam_df = pd.read_csv("data/clean_data.csv", index_col=0)
steam_df


# In[3]:


# set up Mongodb connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn) 

# Declare the database
db = client.steam_db

# Declare the collection
collection = db.top_seller_ratings

# Drop collection to reset database
collection.drop()

# Convert pandas dataframe to dictionary for inserting into MongoDB
data = steam_df.to_dict(orient='records') 

# Insert rows into collection
collection.insert_many(data)


# In[4]:


# Verify results
results = collection.find()
for result in results:
    print(result)

