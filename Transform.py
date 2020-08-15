#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import pymongo


# In[3]:


# Read the csv
top_sellers=pd.read_csv("data/Steam_top_sellers.csv",index_col=0)
top_sellers.head()


# In[9]:


# Read the csv
top_rated=pd.read_csv("data/Steam_games_ratings.csv",index_col=0)
top_rated.head()


# In[7]:


# Merge two dataframes
df=pd.merge(top_sellers,top_rated,on="game_name")
steam_df=df[["game_name","release_date","price","steam_rating"]]
steam_df


# In[10]:


# Drop the games with null values
steam_df.dropna(how="any",axis=0,inplace=True)
steam_df.reset_index(drop=True,inplace=True)
steam_df


# In[11]:


# Split the "price" column
steam_df[["price1","price2","price3"]]=steam_df.price.str.split(" ",expand=True)
steam_df


# In[14]:


for i in range(len(steam_df)):
    steam_df.iloc[i,5]=steam_df.iloc[i,5].replace("CDN$","")
steam_df


# In[15]:


clean_data_df=steam_df[["game_name","release_date","price2","price3","steam_rating"]]
clean_data_df.rename(columns={"price2":"original_price($)","price3":"discount_price($)"},inplace=True)
clean_data_df


# In[16]:


clean_data_df.to_csv("data/clean_data.csv")

